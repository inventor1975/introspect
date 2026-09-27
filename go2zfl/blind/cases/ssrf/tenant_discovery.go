package tenantdiscovery

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type oidcConfig struct {
	Issuer        string `json:"issuer"`
	AuthEndpoint  string `json:"authorization_endpoint"`
	TokenEndpoint string `json:"token_endpoint"`
}

func Discover(c *gin.Context) {
	tenantHost := c.GetHeader("X-Forwarded-Host")
	if tenantHost == "" {
		tenantHost = c.Request.Host
	}
	wellKnown := fmt.Sprintf("https://%s/.well-known/openid-configuration", tenantHost)
	client := &http.Client{Timeout: 4 * time.Second}
	resp, err := client.Get(wellKnown)
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "discovery failed"})
		return
	}
	defer resp.Body.Close()
	var cfg oidcConfig
	if err := json.NewDecoder(resp.Body).Decode(&cfg); err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "invalid discovery document"})
		return
	}
	c.JSON(http.StatusOK, cfg)
}
