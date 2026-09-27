package servicealias

import (
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

var aliases = map[string]string{
	"billing":  "http://billing.internal:7001",
	"catalog":  "http://catalog.internal:7002",
	"shipping": "http://shipping.internal:7003",
}

func resolve(name string) string {
	if base, ok := aliases[name]; ok {
		return base
	}
	return name
}

func Forward(c *gin.Context) {
	base := resolve(c.Query("svc"))
	resp, err := http.Get(base + "/v1/ping")
	if err != nil {
		c.Status(http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	c.Data(resp.StatusCode, "application/json", body)
}
