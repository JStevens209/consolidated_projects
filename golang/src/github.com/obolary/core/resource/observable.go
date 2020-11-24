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
	// KindObservable is the resource kind of the type
	KindObservable Kind = "observable"

	// FactoryObservable is the well-known factory for the type
	FactoryObservable Factory = new(observableFactory).Init()

	// PrototypeObservable is the well-known type (used for reflection)
	PrototypeObservable Observable
)

// ObservableFactory implements Factory
type observableFactory struct {
	FactoryBase
}

// Init initialize the factory
func (observableFactory *observableFactory) Init() *observableFactory {
	log.Trace()
	observableFactory.FactoryBase.SetKind(KindObservable).SetBase(reflect.TypeOf(PrototypeObservable))
	return observableFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (observableFactory *observableFactory) New() interface{} {
	log.Trace()
	return new(Observable).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (observableFactory *observableFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var observable Observable
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&observable); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// get bson-id hex, and set as bson-id
	if observable.Id == "" {
		(&observable).Init()
	} else {
		id := observable.GetId()
		observable.BsonId, _ = primitive.ObjectIDFromHex(id.E)
	}

	// return observable
	return &observable, nil
}

// Observable defines the condition for forwarding an observation
type Observable struct {
	Identity

	// BsonId is used by mongodb for the index
	BsonId primitive.ObjectID `json:"-" bson:"_id,omitempty"`

	// Condition for observable (applied before routing occurs)
	Condition string `json:"condition,omitempty" yaml:"condition,omitempty"`

	// Cron optional pull schedule e.g., * * * 2
	Cron string `json:"cron,omitempty" yaml:"cron,omitempty"`

	// Target optional push URI filter or pull URI
	Target string `json:"target,omitempty" yaml:"target,omitempty"`

	// Template for transform, optional
	Template string `json:"template,omitempty" yaml:"template,omitempty"`
}

// Init initialize the resource
func (observable *Observable) Init() *Observable {
	log.Trace()
	observable.BsonId = primitive.NewObjectID()
	observable.Identity.InitUsingCustomId(KindObservable, observable.BsonId.Hex())
	return observable
}

func (observable *Observable) GetObjectId() primitive.ObjectID {
	return observable.BsonId
}

func (observable *Observable) SetObjectId(bsonId primitive.ObjectID) {
	observable.BsonId = bsonId
}

func (observable *Observable) IsEmptyObjectId() bool {
	return observable.BsonId.IsZero()
}
