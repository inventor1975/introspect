package httpsupgrade

import (
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
)

func CheckTLS(c *gin.Context) {
	raw := c.Query("site")
	u, err := url.Parse(raw)
	if err != nil || u.Host == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "site must be an absolute url"})
		return
	}
	u.Scheme = "https"
	u.Fragment = ""
	resp, err := http.Get(u.String())
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"site": u.Host, "tls": false})
		return
	}
	defer resp.Body.Close()
	expires := ""
	if resp.TLS != nil && len(resp.TLS.PeerCertificates) > 0 {
		expires = resp.TLS.PeerCertificates[0].NotAfter.String()
	}
	c.JSON(http.StatusOK, gin.H{"site": u.Host, "tls": true, "expires": expires})
}
