// Package resource defines all Xero resources
package resource

import (
	"encoding/json"
	"io"
	"time"

	"github.com/obolary/core/log"
)

var (
	// KindFilter is the resource kind of the type
	KindFilter Kind = "filter"

	// FactoryFilter is the well-known factory for the type
	FactoryFilter Factory = new(Filter)
)

// Filter defines the text resource that is formatted as a phone number using the north american numbering plan
// note that the prefixed '$' allows use within other resource types without causing field name ambiquity
//
// Note that all of the filter attributes may be combined to provide more complex queries, e.g., to limit the
// time range of the results the developer would set both LimitAfterInclusive and LimitBefore.
type Filter struct {
	Identity

	// Condition is the filter 'where' clause, e.g., 'name == "foo" && count > 5'
	// TODO - make this a bson.M type, and use "github.com/globalsign/mgo/bson" for query syntax
	Condition map[string]interface{} `json:"$condition,omitempty" yaml:"$condition,omitempty"`

	// LimitNumber of results, e.g., List, optional
	LimitNumber int `json:"$limit_number,omitempty" yaml:"$limit_number,omitempty"`

	// LimitAfterInclusive returns results where the created date-time is newer or equal to the given time
	LimitAfterInclusive time.Time `json:"$limit_after_inclusive,omitempty" yaml:"$limit_after_inclusive,omitempty"`

	// LimitBefore returns results where the created date-time is older than the given time
	LimitBefore time.Time `json:"$limit_before,omitempty" yaml:"$limit_before,omitempty"`

	// Expand results by attribute name (must be an id or ids)
	Expand []string `json:"$expand,omitempty" yaml:"$expand,omitempty"`

	// Collapse resource to required attributes only (depends on kind)
	// mainly used to ignore free-form json extensions (e.g., object)
	Collapse bool `json:"$collapse,omitempty" yaml:"$collapse,omitempty"`

	// Page to return, write-only (WO)
	Page int `json:"$page,omitempty" yaml:"$page,omitempty"`
}

// FactoryFilter interface definition section

// Kind returns the kind of this resource
func (filter *Filter) Kind() Kind {
	return KindFilter
}

// New is a Factory interface function that returns a pointer to a newly initialized resource
func (filter *Filter) New() interface{} {
	return new(Filter).Init()
}

// NewArray is a Factory interface function that returns an empty array or resource pointers
func (filter *Filter) NewArray() interface{} {
	return make([]*Filter, 0, 0)
}

// Append is a Factory interface function that appends a resource pointer to a resource pointer array
func (filter *Filter) Append(objects interface{}, object interface{}) interface{} {

	array, ok := objects.([]*Filter)
	if !ok {
		log.Alarm("could not convert to array")
		return objects
	}
	instance, ok := object.(*Filter)
	if !ok {
		log.Alarm("could not convert to instance")
		return objects
	}
	array = append(array, instance)
	return array
}

// Unmarshal is a Factory interface function that decodes the given data via the reader
// to a resource and returns its pointer
func (filter *Filter) Unmarshal(reader io.Reader) (interface{}, *Error) {

	object := FactoryFilter.New()
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(object); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}
	return object, nil
}

// Filter function definition section

// Init initialize the resource
func (filter *Filter) Init() *Filter {
	filter.Identity.Init(filter.Kind())
	filter.LimitNumber = 100
	filter.Condition = make(map[string]interface{})
	return filter
}
