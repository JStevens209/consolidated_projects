// Package resource defines all Xero resources
package resource

import (
	"encoding/json"
	"io"
	"reflect"

	"github.com/obolary/core/log"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

var (
	// KindObserver is the resource kind of the type
	KindObserver Kind = "observer"

	// FactoryObserver is the well-known factory for the type
	FactoryObserver Factory = new(observerFactory).Init()

	// PrototypeObserver is the well-known type (used for reflection)
	PrototypeObserver Observer
)

// EntityFactory implements Factory
type observerFactory struct {
	FactoryBase
}

// Init initialize the factory
func (observerFactory *observerFactory) Init() *observerFactory {
	log.Trace()
	observerFactory.FactoryBase.SetKind(KindObserver).SetBase(reflect.TypeOf(PrototypeObserver))
	return observerFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (observerFactory *observerFactory) New() interface{} {
	log.Trace()
	return new(Observer).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (observerFactory *observerFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var observer Observer
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&observer); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// get bson-id hex, and set as bson-id
	if observer.Id == "" {
		(&observer).Init()
	} else {
		id := observer.GetId()
		observer.BsonId, _ = primitive.ObjectIDFromHex(id.E)
	}

	// return observer
	return &observer, nil
}

// Observer defines the target of an triggered observation
type Observer struct {
	Identity

	// BsonId is used by mongodb for the index
	BsonId primitive.ObjectID `json:"-" bson:"_id,omitempty"`

	// Target in URL format, i.e., [scheme]://[host]:[port][/path][?query][#fragment]
	// where the scheme can be http, https or kafka.
	Target string `json:"target,omitempty" yaml:"target,omitempty"`

	// Template for transform, optional
	Template string `json:"template,omitempty" yaml:"template,omitempty"`

	// Async drops the request into the common kafka queue to defer the target call
	Async bool `json:"async,omitempty" yaml:"async,omitempty"`

	// Link is an optional URL formatted attribute that can be used for a response channel
	// (i.e., for async responses) or to route the observer response to another observer, etc.
	// TODO - Note this has to potential to cause an infinite loop in the resource manager, requiring http hop counter
	Link string `json:"chain,omitempty"`
}

// Init initialize the resource
func (observer *Observer) Init() *Observer {
	log.Trace()
	observer.BsonId = primitive.NewObjectID()
	observer.Identity.InitUsingCustomId(KindObserver, observer.BsonId.Hex())
	return observer
}

func (observer *Observer) GetObjectId() primitive.ObjectID {
	return observer.BsonId
}

func (observer *Observer) SetObjectId(bsonId primitive.ObjectID) {
	observer.BsonId = bsonId
}

func (observer *Observer) IsEmptyObjectId() bool {
	return observer.BsonId.IsZero()
}
