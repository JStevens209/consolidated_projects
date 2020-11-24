// Package rest contains common consumer/client and producer/server RESTful endpoint definitions
package rest

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"sync"
	"time"

	"github.com/obolary/core/log"

	"github.com/caarlos0/env/v6"
)

// TODO - header tags should merge with context key/value pairs and double as context values (see config.go)
const (
	ActionDelimiter = ":"
	IdParameter     = "/^id"
	IdPathParameter = "/*id"
)

// TODO - these should double as header tags - and passed to the next server
const (
	// outbound
	HeaderTagLatency = "X-Latency"
	HeaderTagCount   = "X-Count"

	// inbound
	CONTEXT_AUTH_ID          = "Authorization"
	CONTEXT_TRANSACTION_ID   = "X-TransactionId"
	CONTEXT_AUTH_ENTITY_ID   = "X-EntityId"
	CONTEXT_AUTH_ENTITY      = "X-Entity"
	CONTEXT_ACCESS_SPACE_IDS = "X-SpaceIds"
	CONTEXT_ACCESS_SPACES    = "X-Spaces"
	CONTEXT_ACCESS_ID        = "X-Id"
	CONTEXT_ACCESS_ACTION    = "X-Action"
	CONTEXT_ACCESS_OBSERVER  = "X-Observer"
	CONTEXT_ACCESS_BODY      = "X-Body"
)

var (
	config *Configuration
	mutex  sync.Mutex
)

type Configuration struct {
	ConsumerFile string `env:"REST_CONSUMER_FILE" envDefault:""`
	HostAndPort  string `env:"REST_HOST_AND_PORT" envDefault:":8080"`
	BasePath     string `env:"REST_BASE_PATH" envDefault:"/gnosko/1.0"`

	TransportMaxIdleConnsPerHost int           `env:"REST_TRANSPORT_MAX_IDLE_CONNS" envDefault:"256"`
	TransportMaxTries            uint          `env:"REST_TRANSPORT_MAX_TRIES" envDefault:"3"`
	TransportRequestTimeout      time.Duration `env:"REST_TRANSPORT_REQUEST_TIMEOUT" envDefault:"60"`

	Consumers map[string]Client
}

func Config() *Configuration {

	if config == nil {

		mutex.Lock()
		if config == nil {

			config = &Configuration{}
			_ = env.Parse(config)

			// attempt to load the consumer configuration
			if config.ConsumerFile != "" {

				data, goerr := ioutil.ReadFile(config.ConsumerFile)
				if goerr != nil {

					log.Alarm("unable to read consumers file, %v due to error, %v", config.ConsumerFile, goerr)

				} else {

					if goerr = json.Unmarshal(data, &(config.Consumers)); goerr != nil {
						log.Alarm("unable to parse consumers file, %v due to error, %v", config.ConsumerFile, goerr)
					}
				}
			} else {
				log.Debug("REST_CONSUMER_FILE not set.")
				log.Debug("Current Env, '%v'", os.Environ())
				log.Debug("Current Config, '%v'", config)
			}
		}
		mutex.Unlock()
	}
	return config
}
