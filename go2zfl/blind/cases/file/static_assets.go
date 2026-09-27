package web

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

var assetsFS = http.Dir("/srv/app/web/assets")

func asset(c *gin.Context) {
	name := c.Query("f")
	if name == "" {
		c.Status(http.StatusBadRequest)
		return
	}
	c.Header("Cache-Control", "public, max-age=31536000, immutable")
	c.FileFromFS(name, assetsFS)
}

func Register(r *gin.Engine) {
	r.GET("/asset", asset)
	r.StaticFS("/static", http.Dir("/srv/app/web/static"))
}
