package projects

import (
	"errors"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
)

var errEscapes = errors.New("path escapes project")

type ProjectFiles struct {
	Root string
}

func (p *ProjectFiles) resolve(rel string) (string, error) {
	full := filepath.Join(p.Root, rel)
	r, err := filepath.Rel(p.Root, full)
	if err != nil {
		return "", err
	}
	if r == ".." || strings.HasPrefix(r, ".."+string(os.PathSeparator)) {
		return "", errEscapes
	}
	return full, nil
}

func (p *ProjectFiles) Read(c *gin.Context) {
	full, err := p.resolve(c.Query("path"))
	if err != nil {
		c.JSON(http.StatusForbidden, gin.H{"error": err.Error()})
		return
	}
	body, err := os.ReadFile(full)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "not found"})
		return
	}
	c.Data(http.StatusOK, "text/plain; charset=utf-8", body)
}

func Mount(r *gin.Engine) {
	p := &ProjectFiles{Root: "/srv/projects/current"}
	r.GET("/project/file", p.Read)
}
