// Package utilities defines xero json helper functions
package utilities

import (
	"bytes"
	"reflect"
	"strings"
)

// ForceJSONArray converts a JSON object into a JSON object array, and ignores the
// conversion if it is already a JSON object array.
func ForceJSONArray(data []byte) ([]byte, bool) {

	isJsonArray := IsJSONArray(data)
	if !isJsonArray {
		head := []byte{'['}
		foot := []byte{']'}
		data = append(head, data...)
		data = append(data, foot...)
	}

	return data, isJsonArray
}

// IsJSONArray will check if the given byte string begins with a JSON array delimiter
func IsJSONArray(data []byte) bool {
	isJsonArray := false
	for _, c := range data {
		if c == '[' {
			isJsonArray = true
			break
		}
		if c != ' ' {
			break
		}
	}
	return isJsonArray
}

// TrimJSON removes JSON tags from the given map
// Note, this is used to remove known JSON fields from a schema-less JSON object
func TrimJSON(original map[string]interface{}, prototypes ...interface{}) map[string]interface{} {

	for _, prototype := range prototypes {
		tof := reflect.TypeOf(prototype)
		for j := 0; j < tof.NumField(); j++ {
			if tag := tof.Field(j).Tag.Get("json"); tag != "" && tag != "-" {
				parts := strings.Split(tag, ",")
				if len(parts) > 0 {
					fieldName := parts[0]
					delete(original, fieldName)
				}
			}
		}
	}
	return original
}

// ConcatJSON concatenates multiple json objects efficiently
//
// Adapted from Go-Swagger,
// https://github.com/go-swagger/go-swagger,
// accessed August 12th, 2015
//
func ConcatJSON(blobs ...[]byte) []byte {

	comma := byte(',')
	closers := map[byte]byte{
		'{': '}',
		'[': ']',
	}

	if len(blobs) == 0 {
		return nil
	}
	if len(blobs) == 1 {
		return blobs[0]
	}

	last := len(blobs) - 1
	var opening, closing byte
	a := 0
	idx := 0
	buf := bytes.NewBuffer(nil)

	for i, b := range blobs {
		if len(b) > 0 && opening == 0 { // is this an array or an object?
			opening, closing = b[0], closers[b[0]]
		}

		if opening != '{' && opening != '[' {
			continue // don't know how to concatenate non container objects
		}

		if len(b) < 3 { // yep empty but also the last one, so closing this thing
			if i == last && a > 0 {
				buf.WriteByte(closing)
			}
			continue
		}

		idx = 0
		if a > 0 { // we need to join with a comma for everything beyond the first non-empty item
			buf.WriteByte(comma)
			idx = 1 // this is not the first or the last so we want to drop the leading bracket
		}

		if i != last { // not the last one, strip brackets
			buf.Write(b[idx : len(b)-1])
		} else { // last one, strip only the leading bracket
			buf.Write(b[idx:])
		}

		a++
	}

	// somehow it ended up being empty, so provide a default value
	if buf.Len() == 0 {
		buf.WriteByte(opening)
		buf.WriteByte(closing)
	}

	return buf.Bytes()
}

func DeepCopyJSON(src map[string]interface{}, dest map[string]interface{}) {
	for key, value := range src {
		switch src[key].(type) {
		case map[string]interface{}:
			dest[key] = map[string]interface{}{}
			DeepCopyJSON(src[key].(map[string]interface{}), dest[key].(map[string]interface{}))
		default:
			dest[key] = value
		}
	}
}
