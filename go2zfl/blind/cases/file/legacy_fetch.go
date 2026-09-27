package legacy

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

const exportRoot = "/srv/erp/exports"

func fetch(c *gin.Context) {
	name := c.Query("name")
	if c.Query("v") == "2" {
		name = filepath.Base(name)
	}
	data, err := os.ReadFile(filepath.Join(exportRoot, name))
	if err != nil {
		c.AbortWithStatus(http.StatusNotFound)
		return
	}
	c.Data(http.StatusOK, "application/octet-stream", data)
}

func Mount(r *gin.Engine) {
	r.GET("/erp/export", fetch)
}
