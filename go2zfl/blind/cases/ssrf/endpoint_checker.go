package endpointchecker

import (
	"context"
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

func TryEndpoint(c *gin.Context) {
	endpoint := strings.TrimSpace(c.PostForm("endpoint"))
	method := strings.ToUpper(c.DefaultPostForm("method", "GET"))

	ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, method, endpoint, nil)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	started := time.Now()
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"ok": false, "error": err.Error()})
		return
	}
	defer resp.Body.Close()
	c.JSON(http.StatusOK, gin.H{
		"ok":       resp.StatusCode < 400,
		"status":   resp.StatusCode,
		"duration": time.Since(started).String(),
		"headers":  resp.Header,
	})
}
