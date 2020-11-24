package middleware

import (
	"net/http"

	"github.com/obolary/core/log"

	"github.com/obolary/gin"
)

func Cors() gin.HandlerFunc {

	return func(context *gin.Context) {
		log.Trace()

		writer := context.Writer
		writer.Header().Set("Access-Control-Allow-Origin", "*")
		writer.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, PATCH, DELETE")
		writer.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")

		if context.Request.Method == "OPTIONS" {

			context.AbortWithStatus(http.StatusOK)
			return
		}

		context.Next()
	}
}
