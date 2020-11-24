// Package rest contains common consumer/client and producer/server RESTful endpoint definitions
package rest

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"strings"
	"time"

	"github.com/obolary/core/log"
	"github.com/obolary/core/resource"

	"github.com/facebookgo/httpcontrol"
	"github.com/obolary/gin"
)

var (
	TlsConfig = &tls.Config{
		InsecureSkipVerify: true,
	}
	HttpControlTransport = &httpcontrol.Transport{
		// WARNING: setting disable-keep-alives to true will invalidate max-idle-conns-per-host
		DisableKeepAlives:   false,
		MaxIdleConnsPerHost: Config().TransportMaxIdleConnsPerHost,
		RequestTimeout:      Config().TransportRequestTimeout * time.Second,
		MaxTries:            Config().TransportMaxTries,
		TLSClientConfig:     TlsConfig,
	}
)

type Client struct {

	// resource kind
	Kind string `json:"kind,omitempty" yaml:"kind,omitempty"`

	// optional field action field
	Actions []string `json:"actions,omitempty" yaml:"action,omitempty"`

	// client schema, host and port
	Target string `json:"target,omitempty" yaml:"target,omitempty"`

	// optional base path
	BasePath string `json:"base_path,omitempty" yaml:"base_path,omitempty"`

	// optional (false) public (not protected)
	// TODO - deprecated
	Public bool `json:"public,omitempty" yaml:"public,omitempty"`

	// optional (false) portal (not managed)
	// TODO - deprecated
	Portal bool `json:"portal,omitempty" yaml:"portal,omitempty"`
}

// TODO - store results from context in header before client call to next service

func Do(request *http.Request) (body []byte, response *http.Response, err *resource.Error) {
	log.Trace()
	// log.Debug("performing request, '%v'", request)

	// create new client each time, but use the same transport
	client := &http.Client{
		Transport: HttpControlTransport,
	}

	// perform the given request
	var goerr error
	response, goerr = client.Do(request)
	if goerr != nil {
		return nil, nil, resource.ErrorBadRequest.Clone(goerr.Error()).Alarm()
	}

	// stream body into memory
	if response.Body != nil {
		if body, goerr = ioutil.ReadAll(response.Body); goerr != nil {
			return nil, nil, resource.ErrorBadRequest.Clone(goerr.Error()).Alarm()
		}
		response.Body.Close()
	}

	// process error response
	if response.StatusCode >= http.StatusBadRequest {

		// default error response
		err = (&resource.Error{
			HttpStatus:  response.StatusCode,
			Code:        strings.Replace(strings.ToLower(http.StatusText(response.StatusCode)), " ", "_", -1),
			Description: string(body),
		}).Init().Debug()

		// attempt to marshal body into resource.Error response
		// failure will cause the default to return
		json.Unmarshal(body, err)

		return nil, nil, err
	}

	// process success response
	return body, response, nil
}

func (client *Client) GetUrl(action, id string) string {

	// build default url (without lookup)
	// TODO, in the future we may do the IP lookup manually
	url := client.Target + client.BasePath + "/" + client.Kind
	if action != "" {
		// TODO - verify the action is on the list if a list is provided
		url = url + ":" + action
	}
	if id != "" {
		url = url + "/" + strings.TrimLeft(id, "/")
	}
	return url
}

// Post the optional object to the url handled by this client
// TODO - context is currently ignored, and may safely be nil
func (client *Client) Post(context *gin.Context, action, id string, in interface{}, params ...string) ([]byte, *resource.Error) {

	// marshal
	var buffer *bytes.Buffer
	if in != nil {
		requestData, goerr := json.Marshal(in)
		if goerr != nil {
			return nil, resource.ErrorBadRequest.Clone(goerr.Error()).Debug()
		}
		buffer = bytes.NewBuffer(requestData)
	} else {
		// note, sending nil will cause panic
		buffer = bytes.NewBuffer([]byte{})
	}

	// build and execute request
	request, goerr := http.NewRequest("POST", client.GetUrl(action, id), buffer)
	if goerr != nil {
		return nil, resource.ErrorBadRequest.Clone(goerr.Error()).Debug()
	}
	request.Header.Set("Content-Type", "application/json")
	if context != nil {
		if authorization := context.Request.Header.Get("Authorization"); authorization != "" {
			request.Header.Set("Authorization", authorization)
		}
	} else if len(params) > 0 {
		if authorization := params[0]; authorization != "" {
			request.Header.Set("Authorization", authorization)
		}
	}

	// build headers from context
	client.contextToHeaders(context, request)

	// perform request
	responseData, response, err := Do(request)
	if err != nil {
		return nil, err
	}

	// build context from headers
	client.headersToContext(context, response)

	// return response
	return responseData, nil
}

// Post the given data
func (client *Client) PostWithRaw(context *gin.Context, action, id, content_type string, buffer *bytes.Buffer) ([]byte, string, *resource.Error) {

	// note, sending nil will cause panic
	if buffer == nil {
		buffer = bytes.NewBuffer([]byte{})
	}

	// build and execute request
	request, goerr := http.NewRequest("POST", client.GetUrl(action, id), buffer)
	if goerr != nil {
		return nil, "", resource.ErrorBadRequest.Clone(goerr.Error()).Debug()
	}
	if content_type != "" {
		request.Header.Set("Content-Type", content_type)
	}
	if context != nil {
		if authorization := context.Request.Header.Get("Authorization"); authorization != "" {
			request.Header.Set("Authorization", authorization)
		}
	}

	// build headers from context
	client.contextToHeaders(context, request)

	// perform request
	responseData, response, err := Do(request)
	if err != nil {
		return nil, "", err
	}

	// build context from headers
	contentTypeReturned := response.Header.Get("Content-Type")
	client.headersToContext(context, response)

	// return response
	return responseData, contentTypeReturned, nil
}

// Post the query string to the url handled by this client
func (client *Client) PostWithQuery(context *gin.Context, action, id, query string) ([]byte, *resource.Error) {

	// note, sending nil will cause panic
	buffer := bytes.NewBuffer([]byte{})

	// build and execute request
	request, goerr := http.NewRequest("POST", client.GetUrl(action, id)+query, buffer)
	if goerr != nil {
		return nil, resource.ErrorBadRequest.Clone(goerr.Error()).Debug()
	}
	request.Header.Set("Content-Type", "application/json")
	if context != nil {
		if authorization := context.Request.Header.Get("Authorization"); authorization != "" {
			request.Header.Set("Authorization", authorization)
		}
	}

	// build headers from context
	client.contextToHeaders(context, request)

	// perform request
	responseData, response, err := Do(request)
	if err != nil {
		return nil, err
	}

	// build context from headers
	client.headersToContext(context, response)

	// return response
	return responseData, nil
}

func (client *Client) contextToHeaders(context *gin.Context, request *http.Request) {

	if context == nil {
		return
	}
	if value, exists := context.Get(CONTEXT_TRANSACTION_ID); exists {
		request.Header.Set(CONTEXT_TRANSACTION_ID, value.(string))
	}
	if value, exists := context.Get(CONTEXT_AUTH_ID); exists {
		request.Header.Set(CONTEXT_AUTH_ID, value.(string))
	}
}

func (client *Client) headersToContext(context *gin.Context, response *http.Response) {
	// TODO - currently context is only one way,...
}
