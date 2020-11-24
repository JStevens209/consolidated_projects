package resource

import (
	"encoding/json"

	"github.com/obolary/core/log"
	"github.com/obolary/core/utilities"
)

type Unknown struct {
	Identity
	Extension map[string]interface{} `json:"-"`
}

func (r Unknown) MarshalJSON() (result []byte, goerr error) {
	log.Trace()

	var identity, extension []byte
	if identity, goerr = json.Marshal(r.Identity); goerr != nil {
		return nil, goerr
	}
	if extension, goerr = json.Marshal(r.Extension); goerr != nil {
		return nil, goerr
	}
	result = utilities.ConcatJSON(identity, extension)

	return result, nil
}

func (r *Unknown) UnmarshalJSON(data []byte) error {
	log.Trace()

	if goerr := json.Unmarshal(data, &r.Identity); goerr != nil {
		return goerr
	}
	var extension map[string]interface{}
	if goerr := json.Unmarshal(data, &extension); goerr != nil {
		return goerr
	}
	r.Extension = utilities.TrimJSON(extension, r.Identity)

	return nil
}
