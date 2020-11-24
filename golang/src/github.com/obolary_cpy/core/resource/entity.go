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
	// KindEntity is the resource kind of the type
	KindEntity Kind = "entity"

	// FactoryEntity is the well-known factory for the type
	FactoryEntity Factory = new(entityFactory).Init()

	// PrototypeEntity is the well-known type (used for reflection)
	PrototypeEntity Entity
)

// EntityFactory implements Factory
type entityFactory struct {
	FactoryBase
}

// Init initialize the factory
func (entityFactory *entityFactory) Init() *entityFactory {
	log.Trace()
	entityFactory.FactoryBase.SetKind(KindEntity).SetBase(reflect.TypeOf(PrototypeEntity))
	return entityFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (entityFactory *entityFactory) New() interface{} {
	log.Trace()
	return new(Entity).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (entityFactory *entityFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var entity Entity
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&entity); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// get bson-id hex, and set as bson-id
	if entity.Id == "" {
		(&entity).Init()
	} else {
		id := entity.GetId()
		entity.BsonId, _ = primitive.ObjectIDFromHex(id.E)
	}

	// return entity
	return &entity, nil
}

// Entity defines the person, place or thing (e.g., person, system, location, application)
// This is not authentication identity (although it may feed into it), but simply
// a reference to a user, user-space or an application for the sake of access control
type Entity struct {
	Identity

	// BsonId is used by mongodb for the index
	BsonId primitive.ObjectID `json:"-" bson:"_id,omitempty"`

	// Url reference to thumbnail image
	// e.g., https://xero.cbre.cloud/xero/1.0/object:create.$thumbnail[/path]/filename.extension
	Thumbnail string `json:"$thumbnail,omitempty" yaml:"$thumbnails,omitempty"`

	// Disabled indicates if the entity is able to sign in or not (default is false)
	IsDisabled bool `json:"is_disabled,omitempty" yaml:"is_disabled,omitempty"`

	// AccessType indicates the oauth access type allowed for this key
	AccessTypes []string `json:"access_types,omitempty" yaml:"access_types,omitempty"`

	// Key is the entity identifier, e.g., open-id, user-name, api-key, etc.
	Key string `json:"key,omitempty" yaml:"key,omitempty" index:"key" unique:"true"`

	// Secret is the optional (hashed) access token (not a password)
	Secret string `json:"secret,omitempty" yaml:"secret,omitempty"`

	// Hint for the secret, optional.
	Hint string `json:"hint,omitempty" yaml:"hint,omitempty"`

	// Uri is the optional redirect uri
	Uri string `json:"uri,omitempty" yaml:"uri,omitempty"`
}

// Init initialize the resource
func (entity *Entity) Init() *Entity {
	log.Trace()
	entity.BsonId = primitive.NewObjectID()
	entity.Identity.InitUsingCustomId(KindEntity, entity.BsonId.Hex())
	return entity
}

func (entity *Entity) GetObjectId() primitive.ObjectID {
	return entity.BsonId
}

func (entity *Entity) SetObjectId(bsonId primitive.ObjectID) {
	entity.BsonId = bsonId
}

func (entity *Entity) IsEmptyObjectId() bool {
	return entity.BsonId.IsZero()
}
