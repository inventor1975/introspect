package support

import (
	"net/http"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

type attachmentQuery struct {
	Ticket int    `form:"ticket" binding:"required,min=1"`
	Name   string `form:"name" binding:"required,alphanum,max=64"`
}

type SupportAPI struct {
	FilesDir string
}

func (s *SupportAPI) Attachment(c *gin.Context) {
	var q attachmentQuery
	if err := c.ShouldBindQuery(&q); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.File(filepath.Join(s.FilesDir, q.Name+".bin"))
}

func (s *SupportAPI) Register(r *gin.Engine) {
	r.GET("/support/attachment", s.Attachment)
}
