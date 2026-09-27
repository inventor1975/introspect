package statusline

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func statusLine(c *gin.Context) {
	service := c.Query("service")
	c.String(http.StatusOK, "<b>%s</b> is operational", service)
}

func Setup(r *gin.Engine) {
	r.GET("/status/line", statusLine)
}
