// Package rest contains common consumer/client and producer/server RESTful endpoint definitions
package rest

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"reflect"
	"strings"
	"time"

	"github.com/obolary/core/log"
	"github.com/obolary/core/resource"

	"github.com/evanphx/json-patch"
	"github.com/obolary/gin"
)

func init() {
	gin.SetMode(gin.ReleaseMode)
}

type serverFactory struct{}

var (
	ServerFactory serverFactory
)

// New creates a new server
func (unused serverFactory) New(router *gin.RouterGroup, factory resource.Factory, producer Producer) *Server {
	return new(Server).Init(router, factory, producer)
}

// Server holds handler information for one resource,
// i.e., each resource has its own server instance.
type Server struct {
	router   *gin.RouterGroup
	factory  resource.Factory
	producer Producer
	kind     resource.Kind
	actions  map[string]*Action
}

// Init the server object
func (server *Server) Init(router *gin.RouterGroup, factory resource.Factory, producer Producer) *Server {
	log.Debug()

	server.router = router
	server.factory = factory
	server.producer = producer
	server.kind = factory.Kind()
	server.actions = make(map[string]*Action)

	// create action routing
	for _, action := range producer.Actions() {

		// establish micro-router for this server
		base := "/" + server.kind.String()
		baseAction := ActionDelimiter + action.Name

		// establish default content-types
		if len(action.ContentTypes) == 0 {
			action.ContentTypes = []string{"application/json"}
		}

		// save the action for quick reference
		server.actions[base+baseAction] = action

		// establish path for this action
		parameterMatch := ""
		if action.ExpectId {
			parameterMatch = IdParameter
			if action.ExpectIdAsPath {
				parameterMatch = IdPathParameter
			}
			baseAction = baseAction + parameterMatch
		}

		// establish alias handler for this action and for well-known actions
		switch action.Name {
		case ActionCreate:
			router.POST(base+baseAction, server.Create)
			log.Debug("created POST handler for, '%v'", base+baseAction)
			router.POST(base+parameterMatch, server.Create)
			log.Debug("created POST handler for, '%v'", base+parameterMatch)
		case ActionDelete:
			router.POST(base+baseAction, server.Delete)
			log.Debug("created POST handler for, '%v'", base+baseAction)
			router.DELETE(base+parameterMatch, server.Delete)
			log.Debug("created DELETE handler for, '%v'", base+parameterMatch)
		case ActionQuery:
			router.POST(base+baseAction, server.Query)
			log.Debug("created POST handler for, '%v'", base+baseAction)
			router.GET(base, server.Query)
			log.Debug("created GET handler for, '%v'", base)
		case ActionGet:
			router.POST(base+baseAction, server.Get)
			log.Debug("created POST handler for, '%v'", base+baseAction)
			router.GET(base+parameterMatch, server.Get)
			log.Debug("created GET handler for, '%v'", base+parameterMatch)
		case ActionSet:
			router.POST(base+baseAction, server.Set)
			log.Debug("created POST handler for, '%v'", base+baseAction)
			router.PUT(base+parameterMatch, server.Set)
			log.Debug("created PUT handler for, '%v'", base+parameterMatch)
		case ActionMerge:
			router.POST(base+baseAction, server.Merge)
			log.Debug("created POST handler for, '%v'", base+baseAction)
			router.PATCH(base+parameterMatch, server.Merge)
			log.Debug("created PATCH handler for, '%v'", base+parameterMatch)
		default:
			router.POST(base+baseAction, server.Act)
			log.Debug("created POST handler for, '%v'", base+baseAction)
		}
	}

	// return myself
	return server
}

// TODO - dont forget batch processing, e.g., json array
// Act performs the custom resource action (i.e., only actions not predefined, such as, ActionCreate, etc)
// (note, conversion from other content-type should have already been done)
func (server *Server) Act(context *gin.Context) {
	log.Debug()

	// handle panic
	defer func() {
		if r := recover(); r != nil {
			err := resource.ErrorInternalServer.Clone("panic, %v", r).Alarm()
			context.JSON(err.HttpStatus, err)
		}
	}()

	// get the resource action from the path
	basePath := server.router.BasePath()
	path := strings.TrimPrefix(context.Request.URL.Path, basePath)
	if index := strings.Index(path[1:], "/"); index > 0 {
		// add one because we started search from one
		// i.e., the final index is off by one
		path = path[:index+1]
	}
	log.Debug("method, '%v'", context.Request.Method)
	log.Debug("path, '%v'", context.Request.URL.Path)
	log.Debug("basePath, '%v'", basePath)
	log.Debug("searching for resource action, '%v'", path)

	// get the the action description
	action, exists := server.actions[path]
	if !exists {
		err := resource.ErrorNotFound.Clone("resource action not found, %v", path).Debug()
		context.JSON(err.HttpStatus, err)
		return
	}
	log.Debug("action, '%v'", action)

	// get the id if one is expected
	var id string
	if action.ExpectId {

		id = context.Param("id")
		if id == "" {

			err := resource.ErrorBadRequest.Clone("request missing expected id").Debug()
			context.JSON(err.HttpStatus, err)
			return
		}
	}
	log.Debug("id, '%v'", id)

	// pass to producer
	if action.Handler == nil {

		err := resource.ErrorInternalServer.Clone("resource handler not found, %v", path).Alarm()
		context.JSON(err.HttpStatus, err)
		return
	}

	// unmarshal body contents if any, note that we always expect json
	in, err := server.content(context, action)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// begin handler latency measurement
	timestamp := time.Now()

	// invoke the handler
	out, err := action.Handler(context, action.Name, id, in)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// end handler latency measurement
	context.Writer.Header().Set(HeaderTagLatency, time.Since(timestamp).String())

	// return no-content response
	if out == nil {
		context.Status(http.StatusNoContent)
		return
	}

	// return content response
	vof := reflect.ValueOf(out)
	switch vof.Kind() {
	case reflect.Array:
	case reflect.Slice:
		context.Writer.Header().Set(HeaderTagCount, fmt.Sprintf("%d", vof.Len()))
	default:
		// do nothing
	}

	// TODO - currently ignoring Accepted header
	// Act is the only handler that allows different accept-types
	// Note that the context might have been updated since the call to the handler
	// this code expects any content type (or blank content type) to be updated if necessary
	// e.g., see xero-data-xero object handler for 'download'.
	if context.ContentType() == "application/json" || context.ContentType() == "" {

		context.JSON(http.StatusOK, out)

	} else {

		buffer, ok := out.(*bytes.Buffer)
		if !ok {
			err := resource.ErrorInternalServer.Clone("unknown type being returned from handler")
			context.JSON(err.HttpStatus, err)
			return
		}
		context.Writer.Write(buffer.Bytes())
	}
}

// Create a new resource using the given object
func (server *Server) Create(context *gin.Context) {
	log.Debug()

	// get the the action
	base := server.kind.String()
	path := "/" + base + ":create"
	action, exists := server.actions[path]
	if !exists {
		err := resource.ErrorNotFound.Clone("resource action not found, %v", path).Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// unmarshal mandatory resource
	in, err := server.content(context, action)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}
	if in == nil {
		err := resource.ErrorBadRequest.Clone("request missing expected resource").Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// route create
	out, err := server.do(context, ActionCreate, resource.EmptyId, in)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// return content
	if out == nil {
		err := resource.ErrorInternalServer.Clone("no content after create").Alarm()
		context.JSON(err.HttpStatus, err)
		return
	}
	context.JSON(http.StatusOK, out)
}

// Delete the resource by id
func (server *Server) Delete(context *gin.Context) {
	log.Debug()

	// get manditory id
	id := context.Param("id")
	if id == "" {
		err := resource.ErrorBadRequest.Clone("request missing expected id").Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// route delete
	_, err := server.do(context, ActionDelete, id, nil)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// always return no-content response
	context.Status(http.StatusNoContent)
}

// Query the resource by optional resource filter
func (server *Server) Query(context *gin.Context) {
	log.Debug()

	// get the the action
	base := server.kind.String()
	path := "/" + base + ":query"
	action, exists := server.actions[path]
	if !exists {
		err := resource.ErrorNotFound.Clone("resource action not found, %v", path).Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// unmarshal optional filter
	in, err := server.content(context, action)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}
	var filter *resource.Filter = nil
	if in != nil {
		log.Debug("setting filter")
		ok := true
		filter, ok = in.(*resource.Filter)
		if !ok {
			log.Debug("failed to cast filter object")
		}
	}

	// if space restricted, enforce restrictions
	var out interface{}
	if filter == nil {

		// TODO - note that interface promotion is occuring if filter is nil, this is why we split,..
		// route get/query
		var err *resource.Error
		out, err = server.do(context, ActionQuery, resource.EmptyId, nil)
		if err != nil {
			context.JSON(err.HttpStatus, err)
			return
		}
	} else {

		// TODO - note that interface promotion is occuring if filter is nil, this is why we split,..
		// route get/query
		var err *resource.Error
		out, err = server.do(context, ActionQuery, resource.EmptyId, filter)
		if err != nil {
			context.JSON(err.HttpStatus, err)
			return
		}
	}

	// return no-content response
	if out == nil {
		context.Status(http.StatusNoContent)
		return
	}

	// add count header tag
	// note return can be either *[]*Type or []*Type
	vof := reflect.ValueOf(out)
	if vof.Kind() == reflect.Ptr {
		vof = vof.Elem()
	}
	switch vof.Kind() {
	case reflect.Array:
	case reflect.Slice:
		context.Writer.Header().Set(HeaderTagCount, fmt.Sprintf("%d", vof.Len()))
	default:
		log.Alarm("unexpected type returned from query, '%v'", vof.Kind())
		context.JSON(http.StatusOK, out)
		return
	}

	// apply expand on identity (i.e., currently only label_ids)
	// in order to expand other attributes, the xero resource manager must
	// implement each supported attribute for the specific resource type
	// TODO - should allow 'get' to perform expand as well
	// TODO - this code should be moved to a function
	if filter != nil && len(filter.Expand) > 0 {

		for _, v := range filter.Expand {

			if v == "label_ids" {

				// create new array to return
				objects := server.factory.NewArray()

				// iterate over all items in the output array,
				// copy each to the new array after added the expanded label
				vof = reflect.ValueOf(out)
				for i := 0; i < vof.Len(); i++ {

					// type conversion requires decode to source type
					// TODO - there has got to be a better way?
					// convert from map to byte array (json is only encoding known, but is slow)
					item := vof.Index(i).Interface()
					data, _ := json.Marshal(item)

					// convert from byte array to instance
					object := server.factory.New()
					_ = json.Unmarshal(data, object)

					// update instance
					// TODO - should cache labels by id to avoid database calls
					if identifier, ok := object.(resource.Identifier); ok && len(identifier.GetLabelIds()) > 0 {

						// filter all labels with the id set to the same value contained in label_ids
						xfilter := &resource.Filter{
							Condition: map[string]interface{}{
								"identity.id": map[string][]string{"$in": identifier.GetLabelIds()},
							},
						}

						// query labels
						client, exists := Config().Consumers[resource.KindLabel.String()]
						if !exists {
							log.Alarm("configuration missing label consumer entry, see Config Consumers")
							continue
						}
						xdata, err := client.Post(context, ActionQuery, resource.EmptyId, xfilter)
						if err != nil {
							log.Alarm("failed to query labels, %v, ignoring,...", err)
							continue
						}

						// convert map to labels and store
						var labels []*resource.Label
						if goerr := json.Unmarshal(xdata, &labels); goerr != nil {
							log.Alarm("failed to unmarshal label query results, %v, ignoring,...", goerr)
							continue
						}

						// set the expanded labels field
						identifier.SetLabels(labels)

					} else {
						log.Alarm("could not convert interface to Identity pointer (%v), ignoring,...", vof.Index(i))
						continue
					}

					// add object to array
					objects = server.factory.Append(objects, object)
				}

				// reset out to the newly created objects array
				// log.Debug("objects, %v", objects)
				out = objects

				// break out of expand search
				break
			}
		}
	}

	// return content response
	context.JSON(http.StatusOK, out)
}

// Get the resource by id
func (server *Server) Get(context *gin.Context) {
	log.Debug()

	// get required id
	id := context.Param("id")
	if id == "" {
		err := resource.ErrorBadRequest.Clone("missing required id parameter").Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// if space restricted, enforce restrictions
	// note, this operation must be idempotent,...
	out, err := server.get(context, id)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// return no-content response
	if out == nil {
		context.Status(http.StatusNoContent)
		return
	}

	context.JSON(http.StatusOK, out)
}

// Set the resource by id to the given object
func (server *Server) Set(context *gin.Context) {
	log.Debug()

	// get mandatory id
	log.Debug("context.Param, %v", context.Param)
	id := context.Param("id")
	if id == "" {
		err := resource.ErrorBadRequest.Clone("request missing expected id").Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// get the the action
	base := server.kind.String()
	path := "/" + base + ":set"
	action, exists := server.actions[path]
	if !exists {
		err := resource.ErrorNotFound.Clone("resource action not found, %v", path).Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// unmarshal mandatory resource
	in, err := server.content(context, action)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}
	if in == nil {
		err := resource.ErrorBadRequest.Clone("request missing expected resource").Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// route set
	out, err := server.do(context, ActionSet, id, in)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// return content
	if out == nil {
		err := resource.ErrorInternalServer.Clone("no content after set").Alarm()
		context.JSON(err.HttpStatus, err)
		return
	}
	context.JSON(http.StatusOK, out)
}

// Merge combines the current resource value attributes with the one given
// This handler is NOT IDEMPOTENT, therefor it will always route to the Set handler
func (server *Server) Merge(context *gin.Context) {
	log.Debug()

	// get mandatory id
	id := context.Param("id")
	if id == "" {
		err := resource.ErrorBadRequest.Clone("request missing expected id").Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// get the current resource object
	// note, this will also check if we have access to the object
	current, err := server.get(context, id)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// check content type
	if context.ContentType() != "application/json" {
		err := resource.ErrorBadRequest.Clone("content type not supported, %v", context.ContentType()).Debug()
		context.JSON(err.HttpStatus, err)
		return
	}

	// merge the current resource with the given object
	document, _ := json.Marshal(current)
	updates, _ := context.GetRawData()
	merge, goerr := jsonpatch.MergePatch(document, updates)
	if goerr != nil {
		err := resource.ErrorBadRequest.Clone("could not merge given JSON, %v", goerr).Debug()
		context.JSON(err.HttpStatus, err)
		return
	}
	buffer := bytes.NewBuffer(merge)

	// unmarshal merged JSON
	var in interface{}
	in, err = server.factory.Unmarshal(buffer)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// route merge as a set (since it's already merged)
	out, err := server.do(context, ActionSet, id, in)
	if err != nil {
		context.JSON(err.HttpStatus, err)
		return
	}

	// return content
	if out == nil {
		err := resource.ErrorInternalServer.Clone("no content after merge").Alarm()
		context.JSON(err.HttpStatus, err)
		return
	}
	context.JSON(http.StatusOK, out)
}

// do routes the given action to the handler if one exists
func (server *Server) do(context *gin.Context, lambda, id string, in interface{}) (interface{}, *resource.Error) {

	// get action from lambda
	base := "/" + server.kind.String()
	action, exists := server.actions[base+ActionDelimiter+lambda]
	if !exists {
		return nil, resource.ErrorNotFound.Clone("action not found, %v", lambda).Debug()
	}

	// begin latency measurement
	timestamp := time.Now()

	// route to handler
	out, err := action.Handler(context, lambda, id, in)
	if err != nil {
		return nil, err
	}

	// end latency measurement
	context.Writer.Header().Set(HeaderTagLatency, time.Since(timestamp).String())

	// return object(s)
	return out, nil
}

// get object by id, space restricted if enabled
func (server *Server) get(context *gin.Context, id string) (interface{}, *resource.Error) {

	// route get/query
	out, err := server.do(context, ActionGet, id, nil)
	if err != nil {
		return nil, err.Debug()
	}
	return out, nil
}

func (server *Server) content(context *gin.Context, action *Action) (interface{}, *resource.Error) {

	if context.Request.ContentLength > 0 && context.Request.Body != nil {

		for _, contentType := range action.ContentTypes {

			if context.ContentType() == contentType {

				switch context.ContentType() {
				case "application/json":

					if action.ExpectFilter {

						return resource.FactoryFilter.Unmarshal(context.Request.Body)

					} else {

						return server.factory.Unmarshal(context.Request.Body)
					}

				default:

					if action.ExpectFilter {

						return nil, resource.ErrorBadRequest.Clone("content type not supported, %v", context.ContentType()).Debug()

					} else {

						data, goerr := ioutil.ReadAll(context.Request.Body)
						if goerr != nil {
							return nil, resource.ErrorBadRequest.Clone("could not read content, %v", goerr).Debug()
						}
						context.Request.Body.Close()

						return bytes.NewBuffer(data), nil
					}
				}
			}
		}
	} else {

		// avoid interface promotion
		// (i.e., a non-nil interface pointing to nil)
		return nil, nil
	}
	return nil, resource.ErrorBadRequest.Clone("content type not supported, %v", context.ContentType()).Debug()
}
