package sandbox

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
)

type Purger struct {
	WorkRoot string
}

func (p *Purger) Purge(c *gin.Context) {
	name := c.PostForm("workspace")
	if name == "" || strings.ContainsAny(name, `/\`) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid workspace name"})
		return
	}
	if err := os.RemoveAll(filepath.Join(p.WorkRoot, name)); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "purge failed"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"purged": name})
}

func Wire(r *gin.Engine) {
	p := &Purger{WorkRoot: "/srv/sandbox/tenants/acme/workspaces"}
	r.POST("/workspaces/purge", p.Purge)
}
