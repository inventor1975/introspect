package jobs

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type Job struct {
	ID     uint   `json:"id"`
	Queue  string `json:"queue"`
	Status string `json:"status"`
}

type JobController struct {
	DB *gorm.DB
}

func (j *JobController) List(c *gin.Context) {
	filters := map[string]interface{}{}
	if s := c.Query("status"); s != "" {
		filters["status"] = s
	}
	if q := c.Query("queue"); q != "" {
		filters["queue"] = q
	}

	var jobs []Job
	if err := j.DB.Where(filters).Order("id desc").Limit(200).Find(&jobs).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "list failed"})
		return
	}
	c.JSON(http.StatusOK, jobs)
}
