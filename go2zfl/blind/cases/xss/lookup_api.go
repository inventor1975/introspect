package lookupapi

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

func lookup(c *gin.Context) {
	term := c.Query("term")
	suggestions := []string{}
	for _, s := range []string{"apple", "apricot", "banana"} {
		if strings.HasPrefix(s, strings.ToLower(term)) {
			suggestions = append(suggestions, s)
		}
	}
	c.JSON(http.StatusOK, gin.H{
		"term":        term,
		"suggestions": suggestions,
		"html":        "<em>" + term + "</em>",
	})
}

func Register(r *gin.Engine) {
	r.GET("/api/lookup", lookup)
}
