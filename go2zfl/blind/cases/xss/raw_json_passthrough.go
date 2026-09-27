package rawjsonpassthrough

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func echoFilter(c *gin.Context) {
	field := c.Query("field")
	value := c.Query("value")
	c.PureJSON(http.StatusOK, gin.H{
		"filter": map[string]string{field: value},
		"hint":   "<b>" + field + "</b> = " + value,
	})
}

func Register(r *gin.Engine) {
	r.GET("/api/filters/echo", echoFilter)
}
