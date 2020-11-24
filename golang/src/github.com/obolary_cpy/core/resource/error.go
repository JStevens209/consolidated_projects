// Package resource defines all Xero resources
package resource

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/obolary/core/log"
)

var (
	// KindError is the resource kind of the type, Error
	KindError Kind = "error"

	// FactoryError is the well-known factory for the type, Error
	FactoryError Factory = new(Error)
)

// Error definition section. Some are generic, however as the codebase matures this list should include 10s to 100s of specific cases
// TODO - should we allow the user to get more information about the error via id, e.g., GET /error/[id]
var (
	// ErrorOk is a generic OK status (i.e., not an error), used for passing OK status in an envelope
	ErrorOk = &Error{HttpStatus: http.StatusOK, Code: "ok", Description: "OK"}

	// ErrorInternalServer is a generic internal-server error, i.e., this server failed to perform an operation
	ErrorInternalServer = &Error{HttpStatus: http.StatusInternalServerError, Code: "internal_server", Description: "internal server error"}

	// ErrorBadRequest is a generic bad-request error, i.e., the client failed to provide valid information
	ErrorBadRequest = &Error{HttpStatus: http.StatusBadRequest, Code: "bad_request", Description: "bad request error"}

	// ErrorBadGateway is a generic bad-gateway error, i.e., a consumed api has failed to perform an operation
	ErrorBadGateway = &Error{HttpStatus: http.StatusBadGateway, Code: "bad_gateway", Description: "bad gateway error"}

	// ErrorNotImplemented is a generic not-implemented error, i.e., the given operation is not ready for consumption
	ErrorNotImplemented = &Error{HttpStatus: http.StatusNotImplemented, Code: "not_implemented", Description: "endpoint not implemented"}

	// ErrorNotFound is a generic not-found error, e.g., the given resource instance reference has not been found
	ErrorNotFound = &Error{HttpStatus: http.StatusNotFound, Code: "not_found", Description: "resource not found"}

	// ErrorForbidden is a generic permission error, e.g., the given authorization header is not valid
	ErrorForbidden = &Error{HttpStatus: http.StatusForbidden, Code: "forbidden", Description: "requested endpoint or resource access forbidden"}
)

// Error is a resource that defines a specific error condition
type Error struct {
	Identity

	// HttpStatus is the recommended status to be returned on a http response
	HttpStatus int `json:"status,omitempty" yaml:"status,omitempty"`

	// Code is the well-defined error code for this error. These are labels, usually in the underscore format, e.g., "not_found"
	Code string `json:"error" yaml:"error" binding:"required"`

	// Description is the specific, human readable description of the error and error-code
	Description string `json:"error_description" yaml:"error_description" binding:"required"`

	// Uri is a optional link to documentation used to mitigate the given error
	Uri string `json:"error_uri,omitempty" yaml:"error_uri,omitempty"`
}

// FactoryTextAddress interface definition section

// Kind returns the kind of this resource
func (xerror *Error) Kind() Kind {
	return KindError
}

// New is a Factory interface function that returns a pointer to a newly initialized resource
func (xerror *Error) New() interface{} {
	return new(Error).Init()
}

// NewArray is a Factory interface function that returns an empty array or resource pointers
func (xerror *Error) NewArray() interface{} {
	return make([]*Error, 0, 0)
}

// Append is a Factory interface function that appends a resource pointer to a resource pointer array
func (xerror *Error) Append(objects interface{}, object interface{}) interface{} {

	array, ok := objects.([]*Error)
	if !ok {
		log.Alarm("could not convert to array")
		return objects
	}
	instance, ok := object.(*Error)
	if !ok {
		log.Alarm("could not convert to instance")
		return objects
	}
	array = append(array, instance)
	return array
}

// Unmarshal is a Factory interface function that decodes the given data via the reader
// to a resource and returns its pointer
func (xerror *Error) Unmarshal(reader io.Reader) (interface{}, *Error) {

	var object Error
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&object); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}
	return &object, nil
}

// Error function definition section

// Init initialize the resource
func (xerror *Error) Init() *Error {
	xerror.Identity.Init(xerror.Kind())
	return xerror
}

// String interface function definition
func (xerror *Error) String() string {
	return fmt.Sprintf("%v: %v", xerror.Code, xerror.Description)
}

// Error interface function definition
func (xerror *Error) Error() string {
	return xerror.String()
}

// Debug is a convenience function which reports the error in the log with a debug severity
func (xerror *Error) Debug() *Error {
	log.Emit(log.LevelDebug, 1, "%s", xerror)
	return xerror
}

// Info is a convenience function which reports the error in the log with a info severity
func (xerror *Error) Info() *Error {
	log.Emit(log.LevelInfo, 1, "%s", xerror)
	return xerror
}

// Alarm is a convenience function which reports the error in the log with a alarm severity
func (xerror *Error) Alarm() *Error {
	log.Emit(log.LevelAlarm, 1, "%s", xerror)
	return xerror
}

// Clone is a convenience function that will clone the given error and replace its
// description with the one provided.
func (serror Error) Clone(args ...interface{}) *Error {
	serror.Init()
	if len(args) > 0 {
		serror.Description = fmt.Sprintf(args[0].(string), args[1:]...)
	}
	return &serror
}
