// Package rest contains common consumer/client and producer/server RESTful endpoint definitions
package rest

import (
	"github.com/obolary/core/log"
	"github.com/obolary/core/resource"

	"github.com/obolary/gin"
)

const (
	IncludeId = true
	ExcludeId = false

	ExpectFilter = true
	ExpectObject = false

	ExpectIdAsPath = true
	ExpectIdAsId   = false
)

// TODO - convert to type, e.g., ActionName
var (
	ActionCreate = "create"
	ActionDelete = "delete"
	ActionQuery  = "query"
	ActionGet    = "get"
	ActionSet    = "set"

	// Note that merge will never receive a handler call, since the server routes
	// all merges to the set handler after the merge is performed.
	ActionMerge = "merge"
)

func ActionCreateBase() *Action {
	return &Action{ActionCreate, nil, ExcludeId, ExpectObject, ExpectIdAsId, []string{"application/json"}}
}

func ActionDeleteBase() *Action {
	return &Action{ActionDelete, nil, IncludeId, ExpectFilter, ExpectIdAsId, []string{"application/json"}}
}

func ActionQueryBase() *Action {
	return &Action{ActionQuery, nil, ExcludeId, ExpectFilter, ExpectIdAsId, []string{"application/json"}}
}

func ActionGetBase() *Action {
	return &Action{ActionGet, nil, IncludeId, ExpectFilter, ExpectIdAsId, []string{"application/json"}}
}

func ActionSetBase() *Action {
	return &Action{ActionSet, nil, IncludeId, ExpectObject, ExpectIdAsId, []string{"application/json"}}
}

func ActionMergeBase() *Action {
	return &Action{ActionMerge, nil, IncludeId, ExpectObject, ExpectIdAsId, []string{"application/json"}}
}

// TODO - this should be the const default - remove same from Action struct
// TODO - deprecate?
var (
	ActionsExpect = map[string]Expect{
		ActionCreate: Expect{false, false},
		ActionDelete: Expect{true, false},
		ActionQuery:  Expect{false, true},
		ActionGet:    Expect{true, false},
		ActionSet:    Expect{true, false},
		ActionMerge:  Expect{true, false},
	}
)

type Expect struct {
	ExpectId     bool `json:"expect_id" yaml:"expect_id"`
	ExpectFilter bool `json:"expect_filter" yaml:"expect_filter"`
}

type Action struct {
	// TODO - name should be type, ActionName?
	Name string `json:"name" yaml:"name"`

	Handler func(context *gin.Context, action, id string, resource interface{}) (interface{}, *resource.Error) `json:"-"`

	ExpectId       bool     `json:"expect_id" yaml:"expect_id"`
	ExpectFilter   bool     `json:"expect_filter" yaml:"expect_filter"`
	ExpectIdAsPath bool     `json:"expect_id_as_path" yaml:"expect_id_as_path"`
	ContentTypes   []string `json:"content_types" yaml:"content_types"`
}

func (action *Action) SetHandler(handler func(context *gin.Context, action, id string, resource interface{}) (interface{}, *resource.Error)) *Action {
	action.Handler = handler
	return action
}

// Producer is an interface which defines common http verbs for each resource
// The Server type provides the basic behavoir of every Producer
type Producer interface {
	Actions() []*Action

	Create(context *gin.Context, action string, id string, object interface{}) (interface{}, *resource.Error)
	Delete(context *gin.Context, action string, id string, object interface{}) (interface{}, *resource.Error)
	Get(context *gin.Context, action string, id string, object interface{}) (interface{}, *resource.Error)
	Set(context *gin.Context, action string, id string, object interface{}) (interface{}, *resource.Error)
	Merge(context *gin.Context, action string, id string, object interface{}) (interface{}, *resource.Error)
}

type ProducerBase struct{}

func (base *ProducerBase) Actions() []*Action {
	log.Debug()
	return []*Action{
		ActionCreateBase().SetHandler(base.Create),
		ActionDeleteBase().SetHandler(base.Delete),
		ActionQueryBase().SetHandler(base.Get),
		ActionGetBase().SetHandler(base.Get),
		ActionSetBase().SetHandler(base.Set),
		ActionMergeBase().SetHandler(base.Merge),
	}
}

func (base *ProducerBase) Create(context *gin.Context, action, id string, object interface{}) (interface{}, *resource.Error) {
	log.Debug()
	return nil, resource.ErrorNotImplemented.Clone()
}

func (base *ProducerBase) Delete(context *gin.Context, action, id string, object interface{}) (interface{}, *resource.Error) {
	log.Debug()
	return nil, resource.ErrorNotImplemented.Clone()
}

func (base *ProducerBase) Get(context *gin.Context, action, id string, object interface{}) (interface{}, *resource.Error) {
	log.Debug()
	return nil, resource.ErrorNotImplemented.Clone()
}

func (base *ProducerBase) Set(context *gin.Context, action, id string, object interface{}) (interface{}, *resource.Error) {
	log.Debug()
	return nil, resource.ErrorNotImplemented.Clone()
}

func (base *ProducerBase) Merge(context *gin.Context, action, id string, object interface{}) (interface{}, *resource.Error) {
	log.Debug()
	return nil, resource.ErrorNotImplemented.Clone()
}
