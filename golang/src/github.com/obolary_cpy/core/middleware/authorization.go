package middleware

import (
	"bytes"
	"encoding/json"
	"io"
	"io/ioutil"
	"strings"

	"github.com/obolary/core/log"
	"github.com/obolary/core/resource"
	"github.com/obolary/core/rest"

	"github.com/obolary/gin"
	"golang.org/x/crypto/bcrypt"
)

type nopCloser struct {
	io.Reader
}

func (nopCloser) Close() error { return nil }

// TODO - store results in context, pass to header before client call to next service
// TODO - check context header values before trying to re-evaluate each middleware (avoid multiple layers)

func Authorization() gin.HandlerFunc {

	// TODO - note that the client_credentials grant-type should not allow access to resources, only create entity (trusted clients only)
	return func(context *gin.Context) {
		log.Debug()

		// get entity consumer
		entityClient, exists := rest.Config().Consumers[resource.KindEntity.String()]
		if !exists {
			err := resource.ErrorInternalServer.Clone("could not determine entity resource endpoint").Alarm()
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}

		var entity resource.Entity
		if Config().EnableAuth {

			// pull authorization header
			var authCode string
			authHeads := context.Request.Header.Get("Authorization")
			if authHeads == resource.Empty {

				// check if this endpoint is public (i.e., meaning, it assumes the xero client id automatically)
				suffix := strings.TrimPrefix(context.Request.URL.Path, rest.Config().BasePath)
				suffix = strings.TrimLeft(suffix, "/")
				slashIndex := strings.Index(suffix, "/")
				if slashIndex > 0 {
					suffix = suffix[:slashIndex]
				}
				client, exists := rest.Config().Consumers[suffix]
				if exists && client.Public {
					log.Debug("missing authorization header, however '%v' is public, using default client-id", suffix)

					// public methods must have client id and secret in body
					var simpleAuth struct {
						ClientId     string `json:"client_id"`
						ClientSecret string `json:"client_secret"`
					}
					var goerr error
					var body []byte
					if context.Request.Body == nil {
						err := resource.ErrorBadRequest.Clone("missing authorization id and secret on JSON content").Debug()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					} else if body, goerr = ioutil.ReadAll(context.Request.Body); goerr != nil {
						err := resource.ErrorBadRequest.Clone("failed to read request body, %v", goerr).Debug()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					} else if goerr := context.Request.Body.Close(); goerr != nil {
						err := resource.ErrorInternalServer.Clone("failed to close request body, %v", goerr).Debug()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					} else if len(body) == 0 {
						err := resource.ErrorBadRequest.Clone("missing required request body").Debug()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					}

					// force reset of request body for handler
					context.Request.Body = nopCloser{bytes.NewBuffer(body)}

					// attempt to determine if credentials are present and valid
					if goerr := json.Unmarshal(body, &simpleAuth); goerr != nil {
						err := resource.ErrorBadRequest.Clone("failed to unmarshal request body, %v", goerr).Debug()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					} else if simpleAuth.ClientId != Config().AuthClientId {
						err := resource.ErrorForbidden.Clone("failed to provide valid credentials").Debug()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					} else if data, err := entityClient.Post(nil, rest.ActionGet, Config().AuthEntityId, nil); err != nil {
						err = resource.ErrorInternalServer.Clone("failed to contact data server, '%v'", err).Alarm()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					} else if goerr := json.Unmarshal(data, &entity); goerr != nil {
						err := resource.ErrorInternalServer.Clone("could not unmarshal entity, '%v'", goerr).Alarm()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					} else if goerr := bcrypt.CompareHashAndPassword([]byte(entity.Secret), []byte(simpleAuth.ClientSecret)); goerr != nil {
						err := resource.ErrorForbidden.Clone("failed to provide valid credentials").Debug()
						context.JSON(err.HttpStatus, err)
						context.Abort()
						return
					}

					goto default_client_id
				}

				err := resource.ErrorForbidden.Clone("missing authorization header").Debug()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return

			} else {

				context.Set(rest.CONTEXT_AUTH_ID, authHeads)
				authParts := strings.Split(authHeads, " ")
				if len(authParts) != 2 {
					err := resource.ErrorForbidden.Clone("authorization header malformed").Debug()
					context.JSON(err.HttpStatus, err)
					context.Abort()
					return
				}
				authCode = authParts[1]
			}

			// get auth-info consumer
			infoClient, exists := rest.Config().Consumers[resource.KindIntrospect.String()]
			if !exists {
				err := resource.ErrorInternalServer.Clone("could not determine authorization information resource endpoint").Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}

			// get token information
			data, err := infoClient.PostWithQuery(nil, resource.Empty, resource.EmptyId, "?code="+authCode)
			if err != nil {
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}

			var token resource.Token
			if goerr := json.Unmarshal(data, &token); goerr != nil {
				err := resource.ErrorInternalServer.Clone("could not unmarshal token, '%v'", goerr).Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}

			// validate token type
			var key string
			switch token.GrantType {
			case "authorization_code":
				fallthrough

			case "token":
				fallthrough

			case "password":
				if token.Email == resource.Empty {
					err = resource.ErrorInternalServer.Clone("token of grant type, '%v' is missing required identity", token.GrantType).Alarm()
					context.JSON(err.HttpStatus, err)
					context.Abort()
					return
				}
				key = token.Email

			case "client_credentials":
				if token.Email != resource.Empty {
					err = resource.ErrorInternalServer.Clone("token of grant type, '%v' includes identity, '%v'", token.GrantType, token.Email).Alarm()
					context.JSON(err.HttpStatus, err)
					context.Abort()
					return
				}
				key = token.ClientId

			case "refresh_token":
				fallthrough

			default:
				// TODO - this error occurs when the token has expired, need to return the correct error instead
				// TODO - handle, {\"error\":\"invalid_grant\",\"error_description\":\"The provided authorization grant (e.g., authorization code, resource owner credentials) or refresh token is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client.\"}

				err = resource.ErrorInternalServer.Clone("token of grant type, '%v' unexpected (%v)", token.GrantType, string(data)).Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}

			// get correct entity
			filter := &resource.Filter{Condition: map[string]interface{}{"key": key}}
			data, err = entityClient.Post(nil, rest.ActionQuery, resource.EmptyId, filter)
			if err != nil {
				err = resource.ErrorInternalServer.Clone("failed to contact data server, %v", err).Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}

			var entities []resource.Entity
			if goerr := json.Unmarshal(data, &entities); goerr != nil {
				err := resource.ErrorInternalServer.Clone("could not unmarshal entity, '%v'", goerr).Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}
			if len(entities) == 0 {
				err = resource.ErrorForbidden.Clone("entity has not been given access to xero").Debug()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}
			if len(entities) > 1 {
				err := resource.ErrorInternalServer.Clone("multiple entities found for one key, '%v'", token.ClientId).Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}

			entity = entities[0]

		} else {
			log.Debug("defaulting to 'authorized'")

			// get authorized entity object
			data, err := entityClient.Post(nil, rest.ActionGet, Config().AuthEntityId, nil)
			if err != nil {
				err = resource.ErrorInternalServer.Clone("failed to contact data server, '%v'", err).Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}

			if goerr := json.Unmarshal(data, &entity); goerr != nil {
				err := resource.ErrorInternalServer.Clone("could not unmarshal entity, '%v'", goerr).Alarm()
				context.JSON(err.HttpStatus, err)
				context.Abort()
				return
			}
		}

	default_client_id:

		if entity.IsDisabled {
			err := resource.ErrorForbidden.Clone("these credentials are currently disabled, this could be due to pending account creation")
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}
		log.Debug("request authorized using, '%v'", entity.Key)

		// TODO - place id and object (as base64 json, i.e., data) in header, x-entity-id, x-entity for /portal, etc

		// set context with entity id and entity object
		context.Set(rest.CONTEXT_AUTH_ENTITY_ID, entity.Id)
		context.Set(rest.CONTEXT_AUTH_ENTITY, &entity)

		context.Next()
	}
}
