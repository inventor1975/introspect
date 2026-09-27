package tickets

import (
	"net/http"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

type AttachmentController struct {
	StorageRoot string
}

func (ac *AttachmentController) Download(c *gin.Context) {
	rel := c.Query("path")
	if rel == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "path required"})
		return
	}
	full := filepath.Join(ac.StorageRoot, "attachments", rel)
	c.FileAttachment(full, filepath.Base(rel))
}

func Mount(r *gin.Engine, ac *AttachmentController) {
	r.GET("/tickets/attachments/download", ac.Download)
}
