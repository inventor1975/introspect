package csvcellpreview

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func cellPreview(c *gin.Context) {
	cell := c.PostForm("cell")
	c.Header("X-Content-Type-Options", "nosniff")
	c.Data(http.StatusOK, "text/csv; charset=utf-8", []byte("value\n\""+cell+"\"\n"))
}

func Routes(r *gin.Engine) {
	r.POST("/import/preview-cell", cellPreview)
}
