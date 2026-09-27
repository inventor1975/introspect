package oembedlookup

import (
	"encoding/json"
	"net/http"
	"net/url"
	"time"

	"github.com/gin-gonic/gin"
)

type lookupRequest struct {
	Provider string `json:"provider" binding:"required"`
	Resource string `json:"resource" binding:"required"`
	MaxWidth int    `json:"max_width"`
}

var client = &http.Client{Timeout: 6 * time.Second}

func Lookup(c *gin.Context) {
	var req lookupRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	q := url.Values{}
	q.Set("url", req.Resource)
	q.Set("format", "json")
	resp, err := client.Get(req.Provider + "?" + q.Encode())
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "provider unreachable"})
		return
	}
	defer resp.Body.Close()
	var embed map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&embed)
	c.JSON(http.StatusOK, embed)
}
