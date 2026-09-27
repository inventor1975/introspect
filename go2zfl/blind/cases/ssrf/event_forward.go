package eventforward

import (
	"bytes"
	"encoding/json"
	"net/http"

	"github.com/gin-gonic/gin"
)

const analyticsIngest = "https://ingest.analytics.acme.io/v1/events"

type clientEvent struct {
	Name       string            `json:"name"`
	URL        string            `json:"url"`
	Referrer   string            `json:"referrer"`
	Properties map[string]string `json:"properties"`
}

func Track(c *gin.Context) {
	var ev clientEvent
	if err := c.BindJSON(&ev); err != nil {
		return
	}
	ev.Properties["ip"] = c.ClientIP()
	buf, _ := json.Marshal(ev)
	resp, err := http.Post(analyticsIngest, "application/json", bytes.NewReader(buf))
	if err != nil {
		c.Status(http.StatusAccepted)
		return
	}
	resp.Body.Close()
	c.Status(http.StatusNoContent)
}
