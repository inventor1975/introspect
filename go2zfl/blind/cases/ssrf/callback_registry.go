package callbackregistry

import (
	"bytes"
	"encoding/json"
	"net/http"
	"slices"

	"github.com/gin-gonic/gin"
)

var registeredCallbacks = []string{
	"https://hooks.slack.com/services/T000/B000/XXXX",
	"https://ops.acme.io/hooks/deploy",
	"https://status.acme.io/api/incidents",
}

func Notify(c *gin.Context) {
	cb := c.PostForm("callback")
	if !slices.Contains(registeredCallbacks, cb) {
		c.JSON(http.StatusForbidden, gin.H{"error": "callback not registered"})
		return
	}
	msg, _ := json.Marshal(gin.H{"text": c.PostForm("message")})
	resp, err := http.Post(cb, "application/json", bytes.NewReader(msg))
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "notify failed"})
		return
	}
	resp.Body.Close()
	c.JSON(http.StatusOK, gin.H{"sent": true})
}
