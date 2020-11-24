// Package resource defines all Xero resources
package resource

import (
	"encoding/base64"
	"encoding/json"
	"time"

	"github.com/obolary/core/log"

	"github.com/google/uuid"
)

const (
	Empty   = ""
	EmptyId = Empty
)

// Kind is a resource type name
// That is, it identifies the schema of the underlying resource
type Kind string

// String interface definition for Kind type
func (kind Kind) String() string {
	return ((string)(kind))
}

type Identifier interface {
	GetId() *Id
	SetId(*Id)
	GetKind() Kind
	SetCreated(time.Time)
	SetUpdated(time.Time)
	GetLabelIds() []string
	SetLabelIds([]string)
	SetLabels([]*Label)
}

// NewUnknownIdentifierByBody unmarshal the given body to an Identifier
// This is a utility function to create an Identity with the remaining JSON as a map
func NewUnknownIdentifierByBody(body []byte) (Identifier, *Error) {
	var identity Unknown
	if goerr := json.Unmarshal(body, &identity); goerr != nil {
		return nil, ErrorBadRequest.Clone("failed to unmarshal content, %v", goerr).Debug()
	}
	return &identity, nil
}

// Identity defines common resource attributes,
// it is embedded in all other resources
type Identity struct {

	// Id is a UUID that identifies the particular resource instance
	Id string `json:"id,omitempty" yaml:"id,omitempty" index:"identity.id" unique:"true"`

	// Kind identifies the schema of this resource
	Kind Kind `json:"kind,omitempty" yaml:"kind,omitempty"`

	// LabelIds Label resource UUIDs attached to this resource (RO via api, RW via config)
	LabelIds []string `json:"label_ids,omitempty" yaml:"label_ids,omitempty" index:"identity.labelids"`

	// Labels Label resource object populated when label_ids are expanded
	Labels []*Label `json:"labels,omitempty" yaml:"labels,omitempty" bson:"-"`

	// Created date and time
	Created time.Time `json:"created,omitempty" yaml:"created,omitempty"`

	// Updated date and time for last update (RO)
	Updated time.Time `json:"updated,omitempty" yaml:"updated,omitempty"`

	// VersionId UUID is an optional id used for optimistic locking
	VersionId string `json:"version_id,omitempty" yaml:"version_id,omitempty"`

	// Documentation provides opt markdown text desribing the resource instance
	Documentation string `json:"documentation,omitempty" yaml:"documentation,omitempty"`

	// SemanticId is an optional id used for structure semantics (e.g, natural language understanding)
	SemanticId string `json:"semantic_id,omitempty" yaml:"semantic_id,omitempty"`
}

// Init (re)initializes the given Identity
func (identity *Identity) Init(kind Kind) *Identity {
	identity.Id = NewId(kind).String()
	identity.Kind = kind
	identity.Created = time.Now()
	identity.Updated = time.Now()
	return identity
}

// InitUsingCustomId initializes the given Identity with a custom id
func (identity *Identity) InitUsingCustomId(kind Kind, id string) *Identity {
	identity.Id = NewCustomId(kind, id).String()
	identity.Kind = kind
	identity.Created = time.Now().UTC()
	identity.Updated = time.Now().UTC()
	return identity
}

// GetId reverts the base64 string back to an id type
func (identity *Identity) GetId() *Id {
	return NewIdFromString(identity.Id)
}

// SetId forces the id to the stringified identifier
func (identity *Identity) SetId(id *Id) {
	identity.Id = id.String()
}

// GetKind returns the underlying kind of this resource
func (identity *Identity) GetKind() Kind {
	return identity.Kind
}

// SetUpdated sets the last update time (UTC)
func (identity *Identity) SetUpdated(utc time.Time) {
	identity.Updated = utc
}

// SetCreated sets the created time (UTC)
func (identity *Identity) SetCreated(utc time.Time) {
	identity.Created = utc
}

// GetLabelIds returns the identity labels
func (identity *Identity) GetLabelIds() []string {
	return identity.LabelIds
}

// SetLabelIds sets the identity labels
func (identity *Identity) SetLabelIds(labels []string) {
	identity.LabelIds = labels
}

// SetLabels sets the expanded label objects
func (identity *Identity) SetLabels(labels []*Label) {
	identity.Labels = labels
}

// Identifier encapsulates the type and reference to a resource
type Id struct {

	// E is the uuid or other object id
	E string `json:"e,omitempty" yaml:"e,omitempty"`

	// K is the kind
	K string `json:"k,omitempty" yaml:"k,omitempty"`
}

// NewId creates a random identifier by kind
func NewId(kind Kind) *Id {
	identifier := Id{
		E: uuid.New().String(),
		K: kind.String(),
	}
	return &identifier
}

// NewCustomId creates an Id from the given values
func NewCustomId(kind Kind, id string) *Id {
	identifier := Id{
		E: id,
		K: kind.String(),
	}
	return &identifier
}

// NewIdFromString creates an Id from the given base64 string (reverse of String())
// If the string is malformed, then nil is returned
func NewIdFromString(encoded string) *Id {
	var id Id
	if data, goerr := base64.StdEncoding.DecodeString(encoded); goerr != nil {
		log.Debug("id malformed, %v", goerr)
		return nil
	} else {
		if goerr = json.Unmarshal(data, &id); goerr != nil {
			log.Debug("id malformed, %v", goerr)
			return nil
		}
	}
	return &id
}

// String converts the identifier to a base64 string
func (id *Id) String() string {
	data, _ := json.Marshal(id)
	return base64.StdEncoding.EncodeToString(data)
}

// Kind returns the kind of the identifier
func (id *Id) Kind() Kind {
	return Kind(id.K)
}

// Id returns the uniq portion of the identifier
func (id *Id) Id() string {
	return id.E
}
