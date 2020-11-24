// Package resource defines all Xero resources
package resource

import (
	"encoding/json"
	"io"
	"reflect"

	"github.com/obolary/core/log"
	"github.com/obolary/core/utilities"
)

type TextTree struct {

	// Text Summary
	Text

	// Tree of Text Blocks
	Tree
}

type Tree struct {
	Pages []*Page `json:"pages,omitempty"`
}

type Page struct {
	Name   string   `json:"name,omitempty"`
	Url    string   `json:"url,omitempty"`
	Width  float64  `json:"width,omitempty"`
	Height float64  `json:"height,omitempty"`
	Blocks []*Block `json:"blocks,omitempty"`
}

type Block struct {
	Text  string `json:"text,omitempty"`
	Token string `json:"token,omitempty"`
	Label string `json:"label,omitempty"`
	Group string `json:"group,omitempty"`

	Box      *Box      `json:"box,omitempty"`
	BoxPixel []*Vertex `json:"vertices,omitempty"`
	Children []*Block  `json:"children,omitempty"`
	Wrangled []*Block  `json:"wrangled,omitempty"`
}

type Box struct {
	Row    float64 `json:"row"`
	Col    float64 `json:"col"`
	Width  float64 `json:"width"`
	Height float64 `json:"height"`
}

type Vertex struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
}

var (
	// KindTextAddress is the resource kind of the type
	KindTextTree Kind = KindObject

	// FactoryTextAddress is the well-known factory for the type
	FactoryTextTree Factory = new(textTreeFactory).Init()

	// PrototypeTextAddress is the well-known type (used for reflection)
	PrototypeTextTree TextTree
)

// PolicyFactory implements Factory
type textTreeFactory struct {
	FactoryBase
}

// Init initialize the factory
func (factory *textTreeFactory) Init() *textTreeFactory {
	log.Trace()
	factory.FactoryBase.SetKind(KindTextTree).SetBase(reflect.TypeOf(PrototypeTextTree))
	return factory
}

// New overrides the FactoryBase Factory interface function
// in order to ensure that the Init function is called
func (factory *textTreeFactory) New() interface{} {
	log.Trace()
	return new(TextTree).Init()
}

// Unmarshal overrides the unmarshaller in order to use a custom id
func (textTreeFactory *textTreeFactory) Unmarshal(reader io.Reader) (interface{}, *Error) {

	// unmarshal
	var textTree TextTree
	decoder := json.NewDecoder(reader)
	if goerr := decoder.Decode(&textTree); goerr != nil {
		return nil, ErrorBadRequest.Clone("could not unmarshal given body, %v", goerr).Debug()
	}

	// return policy
	return &textTree, nil
}

// Init initialize the resource
func (textTree *TextTree) Init() *TextTree {
	log.Trace()
	(&textTree.Text).Init()
	textTree.ObjectType = "tree"
	textTree.Pages = make([]*Page, 0, 0)
	return textTree
}

func (r TextTree) MarshalJSON() (result []byte, goerr error) {
	log.Trace()

	var text, tree []byte
	if text, goerr = json.Marshal(r.Text); goerr != nil {
		return nil, goerr
	}
	if tree, goerr = json.Marshal(r.Tree); goerr != nil {
		return nil, goerr
	}
	return utilities.ConcatJSON(text, tree), nil
}

func (r *TextTree) UnmarshalJSON(data []byte) error {
	log.Trace()

	if goerr := json.Unmarshal(data, &r.Text); goerr != nil {
		return goerr
	}
	if goerr := json.Unmarshal(data, &r.Tree); goerr != nil {
		return goerr
	}
	return nil
}
