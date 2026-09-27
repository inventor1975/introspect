package exports

import (
	"net/http"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

const exportsBase = "/var/exports"

func fetchExport(c *gin.Context) {
	requested := filepath.Clean(c.Query("file"))
	if requested == "." {
		c.Status(http.StatusBadRequest)
		return
	}
	c.File(filepath.Join(exportsBase, requested))
}

func Routes(r *gin.Engine) {
	r.GET("/exports/fetch", fetchExport)
}
