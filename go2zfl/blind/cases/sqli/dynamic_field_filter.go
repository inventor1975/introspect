package vehicles

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type Vehicle struct {
	ID    uint   `json:"id"`
	Make  string `json:"make"`
	Model string `json:"model"`
	Year  int    `json:"year"`
}

type VehicleHandler struct {
	orm *gorm.DB
}

func (h *VehicleHandler) Filter(c *gin.Context) {
	field := c.DefaultQuery("field", "make")
	value := c.Query("value")

	var vs []Vehicle
	err := h.orm.Model(&Vehicle{}).
		Where(field+" = ?", value).
		Limit(100).
		Find(&vs).Error
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "filter failed"})
		return
	}
	c.JSON(http.StatusOK, vs)
}

func Install(r *gin.Engine, db *gorm.DB) {
	h := &VehicleHandler{orm: db}
	r.GET("/vehicles", h.Filter)
}
