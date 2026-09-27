package resultspage

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func results(c *gin.Context) {
	q := c.Query("q")
	page := c.DefaultQuery("page", "1")
	c.HTML(http.StatusOK, "results.tmpl", gin.H{
		"Query": q,
		"Page":  page,
		"Title": "Results for " + q,
	})
}

func Setup() *gin.Engine {
	r := gin.New()
	r.LoadHTMLGlob("templates/*.tmpl")
	r.GET("/search", results)
	return r
}
