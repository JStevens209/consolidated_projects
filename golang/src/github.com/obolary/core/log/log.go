// Package log defines the Xero logging system
package log

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"runtime"
	"strings"
	"time"

	"github.com/facebookgo/httpcontrol"
)

var (
	TlsConfig = &tls.Config{
		InsecureSkipVerify: true,
	}
	HttpControlTransport = &httpcontrol.Transport{
		// WARNING: setting disable-keep-alives to true will invalidate max-idle-conns-per-host
		DisableKeepAlives:   false,
		MaxIdleConnsPerHost: Config().TransportMaxIdleConnsPerHost,
		RequestTimeout:      Config().TransportRequestTimeout * time.Second,
		MaxTries:            Config().TransportMaxTries,
		TLSClientConfig:     TlsConfig,
	}
)

// Level is a bitwise setting indicating the type of log message
type Level int

const (
	// LevelTrace is used to provide the lowest level (i.e., most verbose) level of debugging, esp. used for tracing call-flow.
	// It is only displayed with tracing is turned on.
	LevelTrace Level = 0x01

	// LevelDebug is called when providing information for the developer for context and debugging.
	// It will only be displayed when debugging is turned on.
	LevelDebug Level = 0x02

	// LevelInfo is always displayed (it cannot be turned off), and is typically used to provide context for Alarms.
	LevelInfo Level = 0x04

	// LevelAlarm is always displayed (it cannot be turned off), and is used to notify orchestration and system management that
	// an unexpected critical error has occured and needs attention.
	LevelAlarm Level = 0x08

	// LevelEvent is always displayed (it cannot be turned off), and is used to notify orchestration and system management of
	// a process state transition, e.g., starting up, ready to receive messages, shutting down, etc.
	LevelEvent Level = 0x10

	// LevelMetric is always displayed (it cannot be turned off), and is used to notify orchestration and system management that
	// an tracked value.
	LevelMetric Level = 0x20
)

var (
	logLevelToString = map[Level]string{
		LevelTrace:  "Trace",
		LevelDebug:  "Debug",
		LevelInfo:   "Info",
		LevelAlarm:  "Alarm",
		LevelEvent:  "Event",
		LevelMetric: "Metric",
	}
)

// String converts level to level name
func (level Level) String() string {
	return logLevelToString[level]
}

// Log defines the log-message resource
type Log struct {
	Level     Level     `json:"level"`
	Pc        uintptr   `json:"-"`
	Ip        string    `json:"ip"`
	Timestamp time.Time `json:"timestamp"`
	Process   string    `json:"process"`
	File      string    `json:"file"`
	Line      int       `json:"line"`
	Function  string    `json:"function"`
	Message   string    `json:"message"`
	Metric    string    `json:"metric,omitempty"`
}

// New creates a server-side log message (which may be marshalled)
func New(depth int, level Level, template string, args ...interface{}) *Log {
	return new(Log).Init(depth, level, template, args...)
}

// Init quickly (re)fills the log message details
func (log *Log) Init(depth int, level Level, template string, args ...interface{}) *Log {
	log.Level = level
	log.Ip = Config().PodIp
	log.Timestamp = time.Now().UTC()
	if Config().PodName != "" {
		log.Process = Config().PodName
	} else {
		log.Process = os.Args[0]
	}
	log.Pc, log.File, log.Line, _ = runtime.Caller(depth + 2)
	log.File = log.File[strings.LastIndex(log.File, "/")+1:]
	log.Function = runtime.FuncForPC(log.Pc).Name()
	log.Function = log.Function[strings.LastIndex(log.Function, "/")+1:]
	log.Message = fmt.Sprintf(template, args...)
	log.Metric = ""
	return log
}

// String converts a log message into a formatted string
func (log *Log) String() string {
	fileAndLine := fmt.Sprintf("%v:%v", log.File, log.Line)
	timestamp := log.Timestamp.Format("2006/01/02 15:04:05.999999999")
	name := logLevelToString[log.Level]
	if log.Message == "" {
		return fmt.Sprintf("%v | %v | %v | %v | %v", name, timestamp, log.Process, fileAndLine, log.Function)
	}
	return fmt.Sprintf("%v | %v | %v | %v | %v | %v", name, timestamp, log.Process, fileAndLine, log.Function, log.Message)
}

// ////////////////////////////////////////////////////////////////////////////
// package-wide log implementation

const (
	logLevelMaskTrace Level = LevelMetric | LevelEvent | LevelAlarm | LevelInfo | LevelDebug | LevelTrace
	logLevelMaskDebug Level = LevelMetric | LevelEvent | LevelAlarm | LevelInfo | LevelDebug
	logLevelMaskInfo  Level = LevelMetric | LevelEvent | LevelAlarm | LevelInfo
)

var (
	logLevelMask = logLevelMaskInfo
	logStream    = os.Stdout
	gologWriter  GologWriter
)

var (
	Buffer      []*Log
	BufferIndex = 0
)

// GologWriter is used as a namespace for the Write function
type GologWriter int

// Write provides a means for non-xero based logging to be displayed in our logs.
func (namespace GologWriter) Write(buffer []byte) (n int, err error) {
	Emit(LevelInfo, 4, string(buffer))
	return len(buffer), nil
}

// SetDebugEnabled sets or clears debug logging.
func SetDebugEnabled(isEnabled bool) {
	logLevelMask = logLevelMask & logLevelMaskInfo
	if isEnabled {
		logLevelMask = logLevelMask | LevelDebug
	}
}

// SetTraceEnabled sets or clears trace logging. It is the most verbose mode of logging.
func SetTraceEnabled(isEnabled bool) {
	logLevelMask = logLevelMask & logLevelMaskDebug
	if isEnabled {
		logLevelMask = logLevelMask | LevelTrace
	}
}

// IsDebugEnabled tells the caller if the process is logging debug statements.
func IsDebugEnabled() bool {
	return logLevelMask&LevelDebug != 0x00
}

// Trace is used to provide the lowest level (i.e., most verbose) level of debugging, esp. used for tracing call-flow.
// It is only displayed with tracing is turned on.
func Trace(args ...interface{}) {
	emitWithOperation(LevelTrace, 1, nil, args...)
}

// Debug is called when providing information for the developer for context and debugging.
// It will only be displayed when debugging is turned on.
func Debug(args ...interface{}) {
	emitWithOperation(LevelDebug, 1, nil, args...)
}

// Info is always displayed (it cannot be turned off), and is typically used to provide context for Alarms.
func Info(args ...interface{}) {
	emitWithOperation(LevelInfo, 1, nil, args...)
}

// Alarm is always displayed (it cannot be turned off), and is used to notify orchestration and system management that
// an unexpected critical error has occured and needs attention.
func Alarm(args ...interface{}) {
	emitWithOperation(LevelAlarm, 1, nil, args...)
}

// Event is always displayed (it cannot be turned off), and is used to notify orchestration and system management of
// a process state transition, e.g., starting up, ready to receive messages, shutting down, etc.
func Event(args ...interface{}) {
	emitWithOperation(LevelEvent, 1, nil, args...)
}

// Metric is always displayed (it cannot be turned off), and is used to notify orchestration and system management that
// an tracked value.
func Metric(operation Operation, measurements ...interface{}) {
	operation.Apply(measurements...)
	emitWithOperation(LevelMetric, 1, operation, "%s/%s: %s", operation.GetKind(), operation.GetName(), operation.String())
}

// Emit provides a low-level logging function useful for extending the logging system, an example of this can be
// seen in the Error resource implementation.
func Emit(level Level, stack int, args ...interface{}) {
	emitWithOperation(level, stack+1, nil, args...)
}

// EmitWithOperation provides a low-level logging function useful for extending the logging system
func emitWithOperation(level Level, stack int, operation Operation, args ...interface{}) {

	if level&logLevelMask == level {

		var template string
		if len(args) > 0 {
			var ok bool
			if template, ok = args[0].(string); !ok {
				return
			}
			if len(args) > 1 {
				args = args[1:]
			} else {
				args = nil
			}
		}
		log := New(stack+1, level, template, args...)
		fmt.Fprintf(logStream, "%s\n", log)

		Buffer[BufferIndex] = log
		BufferIndex = (BufferIndex + 1) % Config().BufferSize
		if Config().AggregateLoggingEnabled && level&LevelDebug != LevelDebug && level&LevelTrace != LevelTrace {

			if operation != nil {
				log.Metric = operation.Marshal()
			}

			// TODO - should POST if timeout and buffer-index to avoid thrashing
			var buffer *bytes.Buffer
			if requestData, goerr := json.Marshal(log); goerr != nil {

				fmt.Fprintf(logStream, "%s\n", New(1, LevelAlarm, "failed to marshal log"))

			} else {

				buffer = bytes.NewBuffer(requestData)
				request, goerr := http.NewRequest("POST", Config().AggregateLogUrl, buffer)
				if goerr != nil {

					fmt.Fprintf(logStream, "%s\n", New(1, LevelAlarm, "failed to create log aggregate"))
				}
				client := &http.Client{
					Transport: HttpControlTransport,
				}
				if _, goerr := client.Do(request); goerr != nil {

					fmt.Fprintf(logStream, "%s\n", New(1, LevelAlarm, "failed to send log aggregate"))
				}
			}
		}
	}
}
