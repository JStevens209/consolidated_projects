// Package resource defines all Xero resources
package resource

import (
	"encoding/json"
	"io"

	logger "github.com/obolary/core/log"
)

var (
	// KindLog is the resource kind of the type
	KindLog Kind = "log"

	// FactoryLog is the well-known factory for the type
	FactoryLog Factory = new(Log)
)

// Log defines the system log detail
type Log struct {
	Identity
	logger.Log
}

// FactoryLog interface definition section

// Kind returns the kind of this resource
func (log *Log) Kind() Kind {
	return KindLog
}

// New is a Factory interface function that returns a pointer to a newly initialized resource
func (log *Log) New() interface{} {
	return new(Log).Init()
}

// NewArray is a Factory interface function that returns an empty array or resource pointers
func (log *Log) NewArray() interface{} {
	return make([]*Log, 0, 0)
}

// Append is a Factory interface function that appends a resource pointer to a resource pointer array
func (log *Log) Append(objects interface{}, object interface{}) interface{} {

	array, ok := objects.([]*Log)
	if !ok {
		logger.Alarm("could not convert to array")
		return objects
	}
	instance, ok := object.(*Log)
	if !ok {
		logger.Alarm("could not convert to instance")
		return objects
	}
	array = append(array, instance)
	return array
}

// Unmarshal is a Factory interface function that decodes the given data via the reader
// to a resource and returns its pointer
func (log *Log) Unmarshal(reader io.Reader) (interface{}, *Error) {

	var object Log
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&object); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}
	return &object, nil
}

// Log function definition section

// Init initialize the resource
func (log *Log) Init() *Log {
	log.Identity.Init(log.Kind())
	return log
}
