package gallery

import (
	"html"
	"net/http"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

type Gallery struct {
	ImagesDir string
}

func (g *Gallery) Show(c *gin.Context) {
	img := html.EscapeString(c.Query("img"))
	if img == "" {
		c.String(http.StatusBadRequest, "img parameter missing")
		return
	}
	c.Header("Cache-Control", "public, max-age=86400")
	c.File(filepath.Join(g.ImagesDir, img))
}

func (g *Gallery) Register(r *gin.Engine) {
	r.GET("/gallery/image", g.Show)
}
