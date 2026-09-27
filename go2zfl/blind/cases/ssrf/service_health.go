package servicehealth

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func Health(c *gin.Context) {
	svc := c.Param("service")
	endpoint := "http://" + svc + ".svc.cluster.local:8080/healthz"
	client := http.Client{Timeout: 2 * time.Second}
	resp, err := client.Get(endpoint)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"service": svc, "healthy": false, "reason": err.Error()})
		return
	}
	resp.Body.Close()
	c.JSON(http.StatusOK, gin.H{"service": svc, "healthy": resp.StatusCode == http.StatusOK})
}

func Setup(r *gin.Engine) {
	r.GET("/status/:service", Health)
}
