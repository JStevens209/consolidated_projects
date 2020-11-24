// Package resource defines all Xero resources
package resource

import (
	"encoding/json"
	"io"
	"reflect"

	"github.com/obolary/core/log"
	"github.com/obolary/core/utilities"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

var (
	// KindObject is the resource kind of the type
	KindObject Kind = "object"

	// FactoryObject is the well-known factory for the type
	FactoryObject Factory = new(objectFactory).Init()

	// PrototypeObject is the well-known type (used for reflection)
	PrototypeObject Object
)

// ObjectFactory implements Factory
type objectFactory struct {
	FactoryBase
}

// Init initialize the factory
func (objectFactory *objectFactory) Init() *objectFactory {
	log.Trace()
	objectFactory.FactoryBase.SetKind(KindObject).SetBase(reflect.TypeOf(PrototypeObject))
	return objectFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (objectFactory *objectFactory) New() interface{} {
	log.Trace()
	return new(Object).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (objectFactory *objectFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var object Object
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&object); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// get bson-id hex, and set as bson-id
	if object.Id == "" {
		(&object).Init()
	} else {
		id := object.GetId()
		object.BsonId, _ = primitive.ObjectIDFromHex(id.E)
	}

	// return object
	return &object, nil
}

// Object defines data, either inline or as a reference (e.g., image file)
type Object struct {
	Identity

	// BsonId is used by mongodb for the index
	BsonId primitive.ObjectID `json:"-" bson:"_id,omitempty"`

	// Object meta-data
	ObjectMeta

	// Extension allows undefined schema attributes
	Extension map[string]interface{} `json:"-"`
}

// ObjectMeta data is used to identify the object state, type and opt. location reference
type ObjectMeta struct {

	// Url reference to object data
	// e.g., https://xero.cbre.cloud/xero/1.0/object:create.$content[/path]/filename.extension
	Content string `json:"$content,omitempty" yaml:"$content,omitempty" index:"objectmeta.content"`

	// ContentType of the url, e.g., application/json (default), image/jpeg, text/csv, etc.
	ContentType string `json:"$content_type,omitempty" yaml:"$content_type,omitempty" index:"objectmeta.contenttype"`

	// Url reference to thumbnail image
	// e.g., https://xero.cbre.cloud/xero/1.0/object:create.$thumbnail[/path]/filename.extension
	Thumbnail string `json:"$thumbnail,omitempty" yaml:"$thumbnails,omitempty"`

	// Opt. ObjectType of the object extension, e.g., classification, etc., user defined.
	ObjectType string `json:"$object_type,omitempty" yaml:"object_type,omitempty" index:"objectmeta.objecttype"`

	// Opt. ObjectStore of the object, e.g., mdb (the default if empty), s3, etc.
	ObjectStore string `json:"$object_store,omitempty" yaml:"$object_store,omitempty"`

	// Opt. Action of the observation, e.g., update, depends on the object (RO) - used by streaming
	// TODO - note if Identity.Id is the same as the TransactionId (i.e., X-TransactionId header)?
	Action string `json:"$action,omitempty" yaml:"$action,omitempty" index:"objectmeta.action"`

	// Opt. State of the observation, e.g., pending, complete, etc. (RO) - used by streaming
	State string `json:"$state,omitempty" yaml:"$state,omitempty" index:"objectmeta.state"`

	// Opt. Status of the observation (RO) - used by streaming
	Status *Error `json:"$status,omitempty" yaml:"$status,omitempty"`

	// Image classification
	// TODO: Create an ImageObject, of which this will be an attribute
	Classifications []ClassificationLabel `json:"$classifications,omitempty" yaml:"$classifications,omitempty" index:"objectmeta.classifications"`
}

type ClassificationLabel struct {
	Name       string  `json:"name,omitempty" yaml:"name,omitempty"`
	Confidence float64 `json:"confidence,omitempty" yaml:"confidence,omitempty"`
}

// Init initialize the resource
func (object *Object) Init() *Object {
	log.Trace()
	object.BsonId = primitive.NewObjectID()
	object.Identity.InitUsingCustomId(KindObject, object.BsonId.Hex())
	object.Extension = make(map[string]interface{})
	return object
}

func (object *Object) GetObjectId() primitive.ObjectID {
	return object.BsonId
}

func (object *Object) SetObjectId(bsonId primitive.ObjectID) {
	object.BsonId = bsonId
}

func (object *Object) IsEmptyObjectId() bool {
	return object.BsonId.IsZero()
}

// MarshalJSON is a custom marshaller
func (r Object) MarshalJSON() (result []byte, goerr error) {
	log.Trace()

	var identity, transaction, extension []byte
	if identity, goerr = json.Marshal(r.Identity); goerr != nil {
		return nil, goerr
	}
	if transaction, goerr = json.Marshal(r.ObjectMeta); goerr != nil {
		return nil, goerr
	}
	if extension, goerr = json.Marshal(r.Extension); goerr != nil {
		return nil, goerr
	}
	result = utilities.ConcatJSON(identity, transaction, extension)

	return result, nil
}

// UnmarshalJSON is a custom un-marshaller
func (r *Object) UnmarshalJSON(data []byte) error {
	log.Trace()

	r.Init()
	if goerr := json.Unmarshal(data, &r.Identity); goerr != nil {
		return goerr
	}
	if goerr := json.Unmarshal(data, &r.ObjectMeta); goerr != nil {
		return goerr
	}
	var extension map[string]interface{}
	if goerr := json.Unmarshal(data, &extension); goerr != nil {
		return goerr
	}
	r.Extension = utilities.TrimJSON(extension, r.Identity, r.ObjectMeta)

	return nil
}
