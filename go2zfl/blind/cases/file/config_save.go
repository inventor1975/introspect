package settings

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

type saveProfileReq struct {
	Name    string `json:"name" binding:"required"`
	Content string `json:"content" binding:"required"`
}

type ProfileAPI struct {
	Dir string
}

func (p *ProfileAPI) Save(c *gin.Context) {
	var req saveProfileReq
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	dest := filepath.Join(p.Dir, req.Name+".yaml")
	if err := os.WriteFile(dest, []byte(req.Content), 0o644); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not save"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"saved": req.Name})
}

func Register(g *gin.RouterGroup, p *ProfileAPI) {
	g.PUT("/profiles", p.Save)
}
