package middleware

import (
	"github.com/caarlos0/env/v6"
)

var (
	config *Configuration
)

type Configuration struct {

	// EnableAuth forces authorization checks on the Authorization header tag
	EnableAuth bool `env:"XERO_AUTHORIZATION_ENABLED" envDefault:"true"`

	// EnableAccess forces access control checks on the authorized Entity
	EnableAccess bool `env:"XERO_ACCESS_ENABLED" envDefault:"true"`

	// AuthEntityId is used when EnableAuth is set to false, i.e., it is the default entity
	AuthEntityId string `env:"XERO_CONTEXT_ENTITY_ID" envDefault:"eyJlIjoiNWI1YjQxOGU4MDg0N2QwMDAxOWI1ZTY3IiwiayI6ImVudGl0eSJ9"`

	// Note that this points to the xero-api-client-key
	AuthClientId string `env:"XERO_CONTEXT_CLIENT_ID" envDefault:"xero-api-client-key"`
}

func Config() *Configuration {

	if config == nil {

		// initialize configuration instance
		config = &Configuration{}
		_ = env.Parse(config)
	}
	return config
}
