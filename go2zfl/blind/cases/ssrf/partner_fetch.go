package partnerfetch

import (
	"io"
	"net/http"
	"net/url"
	"strings"

	"github.com/gin-gonic/gin"
)

var partnerHosts = map[string]struct{}{
	"api.northwind-partners.com": {},
	"feeds.contoso-supply.com":   {},
}

func FetchPartnerFeed(c *gin.Context) {
	u, err := url.Parse(c.Query("feed"))
	if err != nil {
		c.AbortWithStatus(http.StatusBadRequest)
		return
	}
	if u.Scheme != "https" || u.User != nil || u.Port() != "" {
		c.AbortWithStatus(http.StatusBadRequest)
		return
	}
	if _, ok := partnerHosts[strings.ToLower(u.Hostname())]; !ok {
		c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error": "unknown partner"})
		return
	}
	resp, err := http.Get(u.String())
	if err != nil {
		c.AbortWithStatus(http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(io.LimitReader(resp.Body, 5<<20))
	c.Data(http.StatusOK, "application/xml", body)
}
