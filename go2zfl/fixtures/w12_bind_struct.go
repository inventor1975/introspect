package fx

import (
	"path/filepath"

	"github.com/gin-gonic/gin"
)

type fileQuery struct {
	Name string `form:"name" binding:"required,alphanum"`
	Dir  string `form:"dir"`
}

func Download(c *gin.Context) {
	var q fileQuery
	if err := c.ShouldBindQuery(&q); err != nil {
		return
	}
	c.File(filepath.Join("/srv/files", q.Name+".bin")) // alphanum: no dots, no separators
	c.File(filepath.Join("/srv/files", q.Dir, "index.bin"))
}
