package inventoryitem

import (
	"fmt"
	"io"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func Item(c *gin.Context) {
	id, err := strconv.Atoi(c.Query("sku"))
	if err != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "sku must be a positive integer"})
		return
	}
	target := fmt.Sprintf("http://inventory.internal:8080/items/%d", id)
	req, _ := http.NewRequest(http.MethodGet, target, nil)
	req.Header.Set("Accept", "application/json")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		c.Status(http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	c.Data(resp.StatusCode, "application/json", body)
}
