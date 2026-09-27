package products

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type Product struct {
	ID    uint    `json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

var allowedSorts = []string{"name", "price", "created_at"}

type ProductController struct {
	db *gorm.DB
}

func (pc *ProductController) Index(c *gin.Context) {
	requested := strings.ToLower(c.DefaultQuery("sort", "name"))

	sort := "name"
	for _, a := range allowedSorts {
		if a == requested {
			sort = requested
			break
		}
	}

	var list []Product
	if err := pc.db.Order(sort).Find(&list).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, list)
}
