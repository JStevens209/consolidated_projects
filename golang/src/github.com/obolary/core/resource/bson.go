// Package resource defines all Xero resources
package resource

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Bsoner interface {
	GetObjectId() primitive.ObjectID
	SetObjectId(primitive.ObjectID)
	IsEmptyObjectId() bool
}
