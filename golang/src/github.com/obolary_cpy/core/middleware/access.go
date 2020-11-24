package middleware

import (
	"encoding/json"
	// "net/http"
	// "strings"

	"github.com/obolary/core/log"
	"github.com/obolary/core/resource"
	"github.com/obolary/core/rest"

	"github.com/obolary/gin"
)

func Access() gin.HandlerFunc {

	return func(context *gin.Context) {
		log.Debug()

		// get entity from context
		object, exists := context.Get(rest.CONTEXT_AUTH_ENTITY)
		if !exists {
			err := resource.ErrorInternalServer.Clone("missing context value, entity").Alarm()
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}
		entity, ok := object.(*resource.Entity)
		if !ok {
			err := resource.ErrorInternalServer.Clone("conversion failed on context object, entity").Alarm()
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}

		// get label consumer client
		labelClient, exists := rest.Config().Consumers[resource.KindLabel.String()]
		if !exists {
			err := resource.ErrorInternalServer.Clone("could not determine label resource endpoint").Alarm()
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}

		// get entity space(s)
		filter := &resource.Filter{
			Condition: map[string]interface{}{
				"identity.id": map[string]interface{}{"$in": entity.LabelIds},
				"name":        "space",
			},
		}
		data, err := labelClient.Post(nil, rest.ActionQuery, resource.EmptyId, filter)
		if err != nil {
			err = resource.ErrorInternalServer.Clone("failed to contact server, '%v'", err.String()).Alarm()
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}
		var spaces []*resource.Label
		if goerr := json.Unmarshal(data, &spaces); goerr != nil {
			err := resource.ErrorInternalServer.Clone("could not unmarshal labels, %v", goerr).Alarm()
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}
		if len(spaces) == 0 {
			err := resource.ErrorInternalServer.Clone("entity does not belong to any space, %v (%v)", entity.Key, entity.Id).Alarm()
			context.JSON(err.HttpStatus, err)
			context.Abort()
			return
		}
		// insure the the first element is always the "owned" space
		space_ids := make([]string, 0, len(spaces))
		for _, labelid := range entity.LabelIds {
			for _, space := range spaces {
				if labelid == space.Id {
					space_ids = append(space_ids, labelid)
					log.Debug("entity '%v' belongs to space, '%v' ('%v')", entity.Key, space.Value, labelid)
				}
			}
		}
		// TODO - place spaces in header as x-entity-spaces base64 json (i.e., data) for /portal

		// set context with entity space(s)
		context.Set(rest.CONTEXT_ACCESS_SPACES, spaces)
		context.Set(rest.CONTEXT_ACCESS_SPACE_IDS, space_ids)

		// TODO - move xero policy checks to here?

		// finish
		context.Next()
	}
}
