package articleslug

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func showArticle(c *gin.Context) {
	slug := c.Param("slug")
	c.Header("Content-Type", "text/html; charset=utf-8")
	c.String(http.StatusNotFound, "<html><body><p>No article named %s was found.</p></body></html>", slug)
}

func Routes(r *gin.Engine) {
	r.GET("/articles/:slug", showArticle)
}
