package workspace

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

var workspacesRoot = "/data/workspaces"

type entry struct {
	Name  string `json:"name"`
	IsDir bool   `json:"dir"`
}

func listWorkspace(c *gin.Context) {
	ws := c.GetHeader("X-Workspace")
	sub := c.DefaultQuery("dir", ".")
	items, err := os.ReadDir(filepath.Join(workspacesRoot, ws, sub))
	if err != nil {
		c.AbortWithStatusJSON(http.StatusNotFound, gin.H{"error": "no such directory"})
		return
	}
	out := make([]entry, 0, len(items))
	for _, it := range items {
		out = append(out, entry{Name: it.Name(), IsDir: it.IsDir()})
	}
	c.JSON(http.StatusOK, out)
}

func Setup(r *gin.Engine) {
	r.GET("/api/workspace/files", listWorkspace)
}
