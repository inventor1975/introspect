package jobrunner

import (
	"bytes"
	"encoding/json"
	"net/http"

	"github.com/gin-gonic/gin"
)

const renderWorker = "http://render-worker.internal:7070/jobs"

type Job struct {
	Template  string                 `json:"template"`
	Data      map[string]interface{} `json:"data"`
	WorkerURL string                 `json:"worker_url"`
}

func Submit(c *gin.Context) {
	var job Job
	if err := c.ShouldBindJSON(&job); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	job.WorkerURL = renderWorker
	payload, _ := json.Marshal(job)
	resp, err := http.Post(job.WorkerURL, "application/json", bytes.NewReader(payload))
	if err != nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "worker unavailable"})
		return
	}
	defer resp.Body.Close()
	c.Status(resp.StatusCode)
}
