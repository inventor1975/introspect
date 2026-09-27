package repostats

import (
	"encoding/json"
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
)

type statsQuery struct {
	Forge string `form:"forge" binding:"required,oneof=github gitlab"`
	Owner string `form:"owner" binding:"required"`
	Repo  string `form:"repo" binding:"required"`
}

var forgeAPIs = map[string]string{
	"github": "api.github.com",
	"gitlab": "gitlab.com",
}

func Stats(c *gin.Context) {
	var q statsQuery
	if err := c.ShouldBindQuery(&q); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	host, ok := forgeAPIs[q.Forge]
	if !ok {
		c.JSON(http.StatusBadRequest, gin.H{"error": "unsupported forge"})
		return
	}
	u := url.URL{Scheme: "https", Host: host, Path: "/repos/" + q.Owner + "/" + q.Repo}
	resp, err := http.Get(u.String())
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "forge unreachable"})
		return
	}
	defer resp.Body.Close()
	var stats map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&stats)
	c.JSON(http.StatusOK, gin.H{"stars": stats["stargazers_count"], "forks": stats["forks_count"]})
}
