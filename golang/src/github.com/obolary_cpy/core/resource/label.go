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
	// KindLabel is the resource kind of the type
	KindLabel Kind = "label"

	// FactoryLabel is the well-known factory for the type
	FactoryLabel Factory = new(labelFactory).Init()

	// PrototypeLabel is the well-known type (used for reflection)
	PrototypeLabel Label

	// Well-known labels

	// LabelNameSpace provides ownership semantics (e.g., account, tenant, delegate, etc)
	LabelNameSpace = "space"
	// LabelNameLambda provides custom behaviors
	LabelNameLambda = "lambda"
	// LabelNameScope defines oauth client scope
	LabelNameScope = "scope"
)

// LabelFactory implements Factory
type labelFactory struct {
	FactoryBase
}

// Init initialize the factory
func (labelFactory *labelFactory) Init() *labelFactory {
	log.Trace()
	labelFactory.FactoryBase.SetKind(KindLabel).SetBase(reflect.TypeOf(PrototypeLabel))
	return labelFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (labelFactory *labelFactory) New() interface{} {
	log.Trace()
	return new(Label).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (labelFactory *labelFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var label Label
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&label); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// get bson-id hex, and set as bson-id
	if label.Id == "" {
		(&label).Init()
	} else {
		id := label.GetId()
		label.BsonId, _ = primitive.ObjectIDFromHex(id.E)
	}

	// return label
	return &label, nil
}

// Label defines resource grouping and associations
type Label struct {
	Identity

	// BsonId is used by mongodb for the index
	BsonId primitive.ObjectID `json:"-" bson:"_id,omitempty"`

	// ObjectIds used for attach and detach requests and are not saved in the database
	// they may also be used to show the index table of the label in the future
	ObjectIds []string `json:"object_ids,omitempty" yaml:"object_ids,omitempty" bson:"-"`

	// Name of the label, which may or may not be unique by namespace (i.e., this labels label)
	Name string `json:"name,omitempty" yaml:"name,omitempty"`

	// Value of the label, optional.
	Value string `json:"value,omitempty" yaml:"value,omitempty"`

	// DEPRECATED - Description of the label, optional. Use Documentation instead
	Description string `json:"description,omitempty" yaml:"description,omitempty"`
}

// Init initialize the resource
func (label *Label) Init() *Label {
	log.Trace()
	label.BsonId = primitive.NewObjectID()
	label.Identity.InitUsingCustomId(KindLabel, label.BsonId.Hex())
	return label
}

func (label *Label) GetObjectId() primitive.ObjectID {
	return label.BsonId
}

func (label *Label) SetObjectId(bsonId primitive.ObjectID) {
	label.BsonId = bsonId
}

func (label *Label) IsEmptyObjectId() bool {
	return label.BsonId.IsZero()
}
