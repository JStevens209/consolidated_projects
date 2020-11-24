// Package resource defines all Xero resources
package resource

import (
	"encoding/json"
	"io"
	"reflect"

	"github.com/obolary/core/log"
	"github.com/obolary/core/utilities"
)

type TextAddress struct {

	// Text Core
	Text

	// Parsed Address (USPS)
	Address
}

type Address struct {
	Normalized      string `json:"normalized,omitempty"`
	HouseName       string `json:"name,omitempty"`
	Street          string `json:"street,omitempty"`
	StreetNumber    string `json:"street_number,omitempty"`
	StreetAltNumber string `json:"street_altnumber,omitempty"`
	StreetPreDir    string `json:"street_predir,omitempty"`
	StreetPostDir   string `json:"street_postdir,omitempty"`
	StreetName      string `json:"street_name,omitempty"`
	StreetType      string `json:"street_type,omitempty"`
	City            string `json:"city,omitempty"`
	State           string `json:"state,omitempty"`
	Zip             string `json:"zip,omitempty"`
}

var (
	// KindTextAddress is the resource kind of the type
	KindTextAddress Kind = KindObject

	// FactoryTextAddress is the well-known factory for the type
	FactoryTextAddress Factory = new(textAddressFactory).Init()

	// PrototypeTextAddress is the well-known type (used for reflection)
	PrototypeTextAddress TextAddress
)

// PolicyFactory implements Factory
type textAddressFactory struct {
	FactoryBase
}

// Init initialize the factory
func (factory *textAddressFactory) Init() *textAddressFactory {
	log.Trace()
	factory.FactoryBase.SetKind(KindTextAddress).SetBase(reflect.TypeOf(PrototypeTextAddress))
	return factory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (factory *textAddressFactory) New() interface{} {
	log.Trace()
	return new(TextAddress).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (textAddressFactory *textAddressFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var textAddress TextAddress
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&textAddress); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// return policy
	return &textAddress, nil
}

// Init initialize the resource
func (textAddress *TextAddress) Init() *TextAddress {
	log.Trace()
	(&textAddress.Text).Init()
	textAddress.ObjectType = "address"
	return textAddress
}

func (r TextAddress) MarshalJSON() (result []byte, goerr error) {
	log.Trace()

	var text, address []byte
	if text, goerr = json.Marshal(r.Text); goerr != nil {
		return nil, goerr
	}
	if address, goerr = json.Marshal(r.Address); goerr != nil {
		return nil, goerr
	}
	return utilities.ConcatJSON(text, address), nil
}

func (r *TextAddress) UnmarshalJSON(data []byte) error {
	log.Trace()

	if goerr := json.Unmarshal(data, &r.Text); goerr != nil {
		return goerr
	}
	if goerr := json.Unmarshal(data, &r.Address); goerr != nil {
		return goerr
	}
	return nil
}
