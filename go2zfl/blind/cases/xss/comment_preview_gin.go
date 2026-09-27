package commentpreview

import (
	"html/template"
	"net/http"

	"github.com/gin-gonic/gin"
)

func previewComment(c *gin.Context) {
	body := c.PostForm("body")
	author := c.PostForm("author")
	c.HTML(http.StatusOK, "comment_preview.tmpl", gin.H{
		"Author": author,
		"Body":   template.HTML(body),
	})
}

func Setup() *gin.Engine {
	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.POST("/comments/preview", previewComment)
	return r
}
