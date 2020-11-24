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
	// KindSemantic is the resource kind of the type
	KindSemantic Kind = "semantic"

	// FactorySemantic is the well-known factory for the type
	FactorySemantic Factory = new(semanticFactory).Init()

	// PrototypeSemantic is the well-known type (used for reflection)
	PrototypeSemantic Semantic
)

// SemanticFactory implements Factory
type semanticFactory struct {
	FactoryBase
}

// Init initialize the factory
func (semanticFactory *semanticFactory) Init() *semanticFactory {
	log.Trace()
	semanticFactory.FactoryBase.SetKind(KindSemantic).SetBase(reflect.TypeOf(PrototypeSemantic))
	return semanticFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (semanticFactory *semanticFactory) New() interface{} {
	log.Trace()
	return new(Semantic).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (semanticFactory *semanticFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var semantic Semantic
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&semantic); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// get bson-id hex, and set as bson-id
	if semantic.Id == "" {
		(&semantic).Init()
	} else {
		id := semantic.GetId()
		semantic.BsonId, _ = primitive.ObjectIDFromHex(id.E)
	}

	// return semantic
	return &semantic, nil
}

// Semantic defines structure semantics
type Semantic struct {
	Identity

	// BsonId is used by mongodb for the index
	BsonId primitive.ObjectID `json:"-" bson:"_id,omitempty"`

	// Type of the associated attribute
	// e.g., number, string, float, boolean, object, array, etc.
	Type string `json:"type,omitempty" yaml:"type,omitempty"`

	// Aliases are optional semantic names (alternate names) used during dependency tree analysis
	// e.g., temperature, thermostat, heat (as in 'turn the heat up to 50'), etc.
	Aliases []string `json:"aliases,omitempty" yaml:"aliases,omitempty"`

	// Unit is the optional units of the type value
	// e.g, celsius, volt, cm, etc.
	Unit string `json:"unit,omitempty" yaml:"unit,omitempty"`

	// Format is used when the type is ambiguous
	// e.g., enum, int, float, none, etc.
	Format string `json:"format,omitempty" yaml:"format,omitempty"`

	// Constraint is used to define valid value ranges
	// e.g., (1.0,2.0], [AM,PM], etc.
	Constraint string `json:"constraint,omitempty" yaml:"constraint,omitempty"`

	// SemanticIds are used when an object type is being defined
	SemanticIds map[string]string `json:"semantic_ids,omitempty" yaml:"semantic_ids,omitempty"`
}

// Init initialize the resource
func (semantic *Semantic) Init() *Semantic {
	log.Trace()
	semantic.BsonId = primitive.NewObjectID()
	semantic.Identity.InitUsingCustomId(KindSemantic, semantic.BsonId.Hex())
	return semantic
}

func (semantic *Semantic) GetObjectId() primitive.ObjectID {
	return semantic.BsonId
}

func (semantic *Semantic) SetObjectId(bsonId primitive.ObjectID) {
	semantic.BsonId = bsonId
}

func (semantic *Semantic) IsEmptyObjectId() bool {
	return semantic.BsonId.IsZero()
}
