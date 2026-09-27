package docs

import (
	"mime"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

const docsRoot = "/opt/handbook/html"

func renderPage(c *gin.Context) {
	page := c.Param("page")
	body, err := os.ReadFile(filepath.Join(docsRoot, page))
	if err != nil {
		c.String(http.StatusNotFound, "page not found")
		return
	}
	ctype := mime.TypeByExtension(filepath.Ext(page))
	if ctype == "" {
		ctype = "text/html; charset=utf-8"
	}
	c.Data(http.StatusOK, ctype, body)
}

func main() {
	r := gin.Default()
	r.GET("/handbook/*page", renderPage)
	r.Run(":8081")
}
