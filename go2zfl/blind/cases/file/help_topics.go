package help

import (
	"embed"
	"net/http"

	"github.com/gin-gonic/gin"
)

//go:embed topics/*.md
var topicsFS embed.FS

func topic(c *gin.Context) {
	name := c.Param("name")
	md, err := topicsFS.ReadFile("topics/" + name + ".md")
	if err != nil {
		c.String(http.StatusNotFound, "no such help topic")
		return
	}
	c.Data(http.StatusOK, "text/markdown; charset=utf-8", md)
}

func Register(r *gin.Engine) {
	r.GET("/help/:name", topic)
}
