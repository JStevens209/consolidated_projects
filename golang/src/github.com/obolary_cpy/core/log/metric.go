// Package log defines the Xero logging system
package log

import (
	"encoding/json"
	"time"
)

type Operation interface {
	Apply(measurements ...interface{})
	Reset()
	GetKind() string
	GetName() string
	String() string
	Marshal() string
}

type Common struct {
	Name    string `json:"name"`
	Kind    string `json:"kind"`
	Summary string `json:"summary"`
}

func (common *Common) GetKind() string {
	return common.Kind
}

func (common *Common) GetName() string {
	return common.Name
}

func (common *Common) String() string {
	return common.Summary
}

func (common *Common) Marshal() string {
	encoding, _ := json.Marshal(common)
	return string(encoding)
}

type Latency struct {
	Common
	Timestamp time.Time     `json:"-"`
	Duration  time.Duration `json:"duration"`
}

func NewLatency(name string) *Latency {
	latency := new(Latency)
	latency.Kind = "latency"
	latency.Name = name
	latency.Timestamp = time.Now()
	return latency
}

func (latency *Latency) Apply(measurements ...interface{}) {
	latency.Duration = time.Since(latency.Timestamp)
	latency.Summary = latency.Duration.String()
}

func (latency *Latency) Reset() {
	latency.Summary = ""
	latency.Timestamp = time.Now()
}

type Constant struct {
	Common
	Constant map[string]interface{} `json:"constant"`
}

func NewConstant(name string) *Constant {
	constant := new(Constant)
	constant.Kind = "constant"
	constant.Name = name
	constant.Summary = ""
	constant.Constant = make(map[string]interface{})
	return constant
}

func (constant *Constant) Apply(measurements ...interface{}) {

	var name string
	var ok bool
	for i, v := range measurements {

		switch i % 2 {
		case 0:
			if name, ok = v.(string); !ok {
				Alarm("constant expects name value pairs in measurement array")
				return
			}
		case 1:
			constant.Constant[name] = v
		}
	}
}

func (constant *Constant) String() string {
	data, _ := json.Marshal(constant.Constant)
	constant.Summary = string(data)
	return constant.Summary
}

func (constant *Constant) Reset() {
	constant.Constant = nil
	constant.Summary = ""
}
