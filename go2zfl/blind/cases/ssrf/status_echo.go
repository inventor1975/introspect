package statusecho

import (
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

const (
	primaryStatus   = "https://status.acme.io/api/v2/summary.json"
	secondaryStatus = "https://status-backup.acme.io/api/v2/summary.json"
)

func Status(c *gin.Context) {
	page := c.DefaultQuery("page", primaryStatus)
	if page != primaryStatus && page != secondaryStatus {
		c.JSON(http.StatusBadRequest, gin.H{"error": "unknown status page"})
		return
	}
	resp, err := http.Get(page)
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "status page unreachable"})
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	c.Data(http.StatusOK, "application/json", body)
}
