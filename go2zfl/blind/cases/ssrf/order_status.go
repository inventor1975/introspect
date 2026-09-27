package orderstatus

import (
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

type OrderClient struct {
	http *http.Client
	base string
}

func NewOrderClient() *OrderClient {
	return &OrderClient{http: &http.Client{Timeout: 4 * time.Second}, base: "http://orders.internal:8000"}
}

func (o *OrderClient) status(id int64) (int, error) {
	resp, err := o.http.Get(fmt.Sprintf("%s/orders/%d/status", o.base, id))
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()
	return resp.StatusCode, nil
}

func StatusHandler(oc *OrderClient) gin.HandlerFunc {
	return func(c *gin.Context) {
		id, err := strconv.ParseInt(c.Param("id"), 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid order id"})
			return
		}
		code, err := oc.status(id)
		if err != nil {
			c.JSON(http.StatusBadGateway, gin.H{"error": "orders unavailable"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"order": id, "upstream": code})
	}
}
