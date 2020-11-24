// Package resource defines all Xero resources
package resource

import (
	"github.com/obolary/core/log"
)

var (
	// KindToken is the resource kind of the type
	KindToken      Kind = "token"
	KindAuthorize  Kind = "authorize"
	KindIntrospect Kind = "introspect"
	KindInfo       Kind = "info"

	// FactoryToken is the well-known factory for the type
	FactoryToken Factory = new(tokenFactory).Init()

	// PrototypeToken is the well-known type (used for reflection)
	PrototypeToken Token
)

// TokenFactory implements Factory
type tokenFactory struct {
	FactoryBase
}

// Init initialize the factory
func (tokenFactory *tokenFactory) Init() *tokenFactory {
	log.Trace()
	return tokenFactory
}

// Token
type Token struct {
	Error
	AccessToken     string `json:"access_token,omitempty"`
	ClientId        string `json:"client_id,omitempty"`
	Email           string `json:"email,omitempty",omitempty`
	GrantType       string `json:"grant_type",omitempty`
	CustomParameter int    `json:"custom_parameter,omitempty"`
	ExpiresIn       int    `json:"expires_in,omitempty"`
	RefreshToken    string `json:"refresh_token,omitempty"`
	Scope           string `json:"scope,omitempty"`
	TokenType       string `json:"token_type,omitempty"`
}
