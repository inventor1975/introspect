package reports

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type SalesReport struct {
	ID        uint
	Region    string
	Amount    float64
	CreatedAt time.Time
}

type ReportController struct {
	db *gorm.DB
}

func NewReportController(db *gorm.DB) *ReportController {
	return &ReportController{db: db}
}

func (rc *ReportController) List(c *gin.Context) {
	sortBy := c.DefaultQuery("sort", "created_at desc")

	var reports []SalesReport
	if err := rc.db.Order(sortBy).Limit(100).Find(&reports).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, reports)
}

func (rc *ReportController) Mount(g *gin.RouterGroup) {
	g.GET("/reports", rc.List)
}
