package resource

import (
	"encoding/json"
	"io"
	"reflect"

	"github.com/obolary/core/log"
	"github.com/obolary/core/utilities"
)

var (
	// KindText is the resource kind of the type
	KindText Kind = KindObject

	// FactoryText is the well-known factory for the type
	FactoryText Factory = new(textFactory).Init()

	// PrototypeText is the well-known type (used for reflection)
	PrototypeText Text
)

// TextFactory implements Factory
type textFactory struct {
	FactoryBase
}

// Init initialize the factory
func (textFactory *textFactory) Init() *textFactory {
	log.Trace()
	textFactory.FactoryBase.SetKind(KindText).SetBase(reflect.TypeOf(PrototypeText))
	return textFactory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (textFactory *textFactory) New() interface{} {
	log.Trace()
	return new(Text).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (textFactory *textFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var text Text
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&text); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// return text
	return &text, nil
}

// Text
type Text struct {

	// Object core
	Object

	// TextContent
	TextContent
}

// TextContent contains the text
type TextContent struct {

	// Texts is the actual text
	Texts string `json:"text,omitempty"`
}

// Init initialize the resource
func (text *Text) Init() *Text {
	log.Trace()
	(&text.Object).Init()
	text.ObjectType = "text"
	return text
}

func (r Text) MarshalJSON() (result []byte, goerr error) {
	log.Trace()

	// clear extension before marshalling
	r.Extension = make(map[string]interface{})

	var object, text []byte
	if object, goerr = json.Marshal(r.Object); goerr != nil {
		return nil, goerr
	}
	if text, goerr = json.Marshal(r.TextContent); goerr != nil {
		return nil, goerr
	}
	return utilities.ConcatJSON(object, text), nil
}

func (r *Text) UnmarshalJSON(data []byte) error {
	log.Trace()

	if goerr := json.Unmarshal(data, &r.Object); goerr != nil {
		return goerr
	}
	if goerr := json.Unmarshal(data, &r.TextContent); goerr != nil {
		return goerr
	}
	return nil
}
