package expenses

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

const receiptsDir = "/var/expenses/receipts"

func receiptImage(c *gin.Context) {
	id, err := uuid.Parse(c.Query("receipt"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "receipt must be a uuid"})
		return
	}
	path := filepath.Join(receiptsDir, id.String()+".jpg")
	if _, err := os.Stat(path); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "no receipt"})
		return
	}
	c.File(path)
}

func Register(r *gin.Engine) {
	r.GET("/expenses/receipt", receiptImage)
}
