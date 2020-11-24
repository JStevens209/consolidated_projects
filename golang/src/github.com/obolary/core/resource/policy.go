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
	// KindPolicy is the resource kind of the type
	KindPolicy Kind = "policy"

	// FactoryPolicy is the well-known factory for the type
	FactoryPolicy Factory = new(policyFactory).Init()

	// PrototypePolicy is the well-known type (used for reflection)
	PrototypePolicy Policy
)

// PolicyFactory implements Factory
type policyFactory struct {
	FactoryBase
}

// Init initialize the factory
func (policyFactory *policyFactory) Init() *policyFactory {
	log.Trace()
	policyFactory.FactoryBase.SetKind(KindPolicy).SetBase(reflect.TypeOf(PrototypePolicy))
	return policyFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (policyFactory *policyFactory) New() interface{} {
	log.Trace()
	return new(Policy).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (policyFactory *policyFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var policy Policy
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&policy); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// get bson-id hex, and set as bson-id
	if policy.Id == "" {
		(&policy).Init()
	} else {
		id := policy.GetId()
		policy.BsonId, _ = primitive.ObjectIDFromHex(id.E)
	}

	// return policy
	return &policy, nil
}

// Scope defines basic grant or deny conditions
type Policy struct {
	Identity

	// BsonId is used by mongodb for the index
	BsonId primitive.ObjectID `json:"-" bson:"_id,omitempty"`

	// Grant or deny policy type
	Grant bool `json:"grant" yaml:"grant"`

	// Condition is an optional filter using the condition grammar
	Condition string `json:"condition,omitempty" yaml:"condition,omitempty"`

	// Priority is the means of grouping policy evaluations
	// That is, the lowest priority is evaluated first, the same priorities are
	// evaluated as a group (grant all or deny)
	Priority int `json:"priority" yaml:"priority"`
}

// Init initialize the resource
func (policy *Policy) Init() *Policy {
	log.Trace()
	policy.BsonId = primitive.NewObjectID()
	policy.Identity.InitUsingCustomId(KindPolicy, policy.BsonId.Hex())
	return policy
}

func (policy *Policy) GetObjectId() primitive.ObjectID {
	return policy.BsonId
}

func (policy *Policy) SetObjectId(bsonId primitive.ObjectID) {
	policy.BsonId = bsonId
}

func (policy *Policy) IsEmptyObjectId() bool {
	return policy.BsonId.IsZero()
}
