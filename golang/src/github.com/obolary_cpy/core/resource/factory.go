// Package resource defines core Xero resources
package resource

import (
	"encoding/json"
	"io"
	"reflect"

	"github.com/obolary/core/log"
)

// Factory by Kind
var (
	factoryByKind = map[Kind]Factory{
		KindEntity:      FactoryEntity,
		KindError:       FactoryError,
		KindFilter:      FactoryFilter,
		KindLabel:       FactoryLabel,
		KindLog:         FactoryLog,
		KindObject:      FactoryObject,
		KindText:        FactoryText,
		KindTextTree:    FactoryTextTree,
		KindTextAddress: FactoryTextAddress,
		KindObserver:    FactoryObserver,
		KindPolicy:      FactoryPolicy,
		KindSemantic:    FactorySemantic,
		KindToken:       FactoryToken,
		KindObservable:  FactoryObservable,
	}
)

func GetFactoryByKind(kind Kind) (Factory, bool) {
	factory, exists := factoryByKind[kind]
	return factory, exists
}

// Factory is a resource creation utility, it is defined by each resource embedded by Identity
// This interface is used by rest package in order to avoid typing (and reflection) in common
// resource handler implementations
type Factory interface {

	// Kind returns the kind of the resource
	Kind() Kind

	// New is a Factory interface function that returns a pointer to a newly initialized resource
	New() interface{}

	// NewArray is a Factory interface function that returns an empty array or resource pointers
	NewArray() interface{}

	// Append is a Factory interface function that appends a resource pointer to a resource pointer array
	Append(objects interface{}, object interface{}) interface{}

	// Unmarshal reads the given reader, and converts it into the
	// appropriate resource struct. This function must return the
	// unmarshaled resource as a pointer (e.g., *resource.Person, etc)
	// TODO - should we allow return either instance or array based on JSON content?
	Unmarshal(reader io.Reader) (interface{}, *Error)
}

type FactoryBase struct {
	kind Kind
	base reflect.Type
}

func (factory *FactoryBase) Kind() Kind {
	log.Trace()
	return factory.kind
}

func (factory *FactoryBase) SetKind(kind Kind) *FactoryBase {
	log.Trace()
	factory.kind = kind
	return factory
}

func (factory *FactoryBase) Base() reflect.Type {
	log.Trace()
	return factory.base
}

func (factory *FactoryBase) SetBase(base reflect.Type) *FactoryBase {
	log.Trace()
	factory.base = base
	return factory
}

// New will create and return a *Type
func (factory *FactoryBase) New() interface{} {
	log.Trace()
	return reflect.New(factory.base).Interface()
}

// NewArray will create and return a []*Type
func (factory *FactoryBase) NewArray() interface{} {
	log.Trace()

	ptr_type_of_type := reflect.PtrTo(factory.base)
	slice_type := reflect.SliceOf(ptr_type_of_type)
	slice := reflect.MakeSlice(slice_type, 0, 0)
	slice_value := reflect.New(slice_type)
	slice_value.Elem().Set(slice)
	return slice_value.Elem().Interface()
}

// Append will append the given *Type (i.e., object) to the given []*Type (i.e., objects)
func (factory *FactoryBase) Append(objects interface{}, object interface{}) interface{} {
	log.Trace()

	value := reflect.ValueOf(objects)
	value = reflect.Append(value, reflect.ValueOf(object))
	return value.Interface()
}

// Unmarshal the given json data stream to an object
func (factory *FactoryBase) Unmarshal(reader io.Reader) (interface{}, *Error) {
	log.Trace()

	object := factory.New()
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(object); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	return object, nil
}
