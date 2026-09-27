package cdnorigin

import (
	"io"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

const cdnDomain = "acme-cdn.net"

func PullOrigin(c *gin.Context) {
	origin := c.Query("origin")
	if !strings.Contains(origin, cdnDomain) {
		c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error": "origin must be on the cdn"})
		return
	}
	resp, err := http.Get(origin)
	if err != nil {
		c.AbortWithStatus(http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	data, _ := io.ReadAll(resp.Body)
	c.Data(resp.StatusCode, resp.Header.Get("Content-Type"), data)
}

func Register(g *gin.RouterGroup) {
	g.GET("/cdn/pull", PullOrigin)
}
