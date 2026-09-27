package tickets

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type Ticket struct {
	ID       uint   `json:"id"`
	Subject  string `json:"subject"`
	Status   string `json:"status"`
	Assignee string `json:"assignee"`
}

var DB *gorm.DB

func ticketsByStatus(c *gin.Context) {
	status := c.Param("status")
	assignee := c.Query("assignee")

	sqlText := "SELECT id, subject, status, assignee FROM tickets WHERE status = '" + status + "'"
	if assignee != "" {
		sqlText += " AND assignee = '" + assignee + "'"
	}

	var out []Ticket
	if err := DB.Raw(sqlText).Scan(&out).Error; err != nil {
		c.AbortWithStatus(http.StatusInternalServerError)
		return
	}
	c.JSON(http.StatusOK, out)
}

func SetupRoutes(r *gin.Engine) {
	r.GET("/tickets/status/:status", ticketsByStatus)
}
