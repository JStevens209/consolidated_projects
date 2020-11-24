// Package log contains common consumer/client and producer/server RESTful endpoint definitions
package log

import (
	golog "log"
	"time"

	"github.com/caarlos0/env/v6"
)

var (
	config *Configuration
)

// Configuration definition for log package
type Configuration struct {

	// MagicEnabled is used to enable various manual debugging tests and flows, defined by the
	// developer and may differ in meaning from case to case.
	MagicEnabled bool `env:"LOG_MAGIC_ENABLED" envDefault:"false"`

	// TraceEnabled turns on and off full debug function tracing, and in most cases 3rd party debug
	// logs (e.g., database client logging)
	TraceEnabled bool `env:"LOG_TRACE_ENABLED" envDefault:"false"`

	// DebugEnabled enables normal debug logs (alarm and info are always on)
	DebugEnabled bool `env:"LOG_DEBUG_ENABLED" envDefault:"true"`

	// BufferSize is used for the most recent log cache, used in debugging via the API
	BufferSize int `env:"LOG_BUFFER_SIZE" envDefault:"25"`

	// Pod Information
	PodName string `env:"POD_NAME" envDefault:""`
	PodIp   string `env:"POD_IP" envDefault:""`

	// Log Aggregation
	AggregateLogUrl         string `env:"LOG_AGGREGATION_URL" envDefault:"http://log-service.obolary.svc.cluster.local:8080/gnosko/1.0/log:create"`
	AggregateLoggingEnabled bool   `env:"LOG_AGGREGATION_ENABLED" envDefault:"true"`

	// Log Aggregation Transport
	TransportMaxIdleConnsPerHost int           `env:"REST_TRANSPORT_MAX_IDLE_CONNS" envDefault:"256"`
	TransportMaxTries            uint          `env:"REST_TRANSPORT_MAX_TRIES" envDefault:"3"`
	TransportRequestTimeout      time.Duration `env:"REST_TRANSPORT_REQUEST_TIMEOUT" envDefault:"60"`
}

// Don't do lazy eval
func init() {
	_ = Config()
}

// Config accessor
func Config() *Configuration {

	if config == nil {

		config = &Configuration{}
		_ = env.Parse(config)

		if config.DebugEnabled {
			logLevelMask = logLevelMaskDebug
		}
		if config.TraceEnabled {
			logLevelMask = logLevelMaskTrace
		}

		Buffer = make([]*Log, config.BufferSize, config.BufferSize)
		BufferIndex = 0

		golog.SetOutput(gologWriter)
	}
	return config
}
