package history

import (
	"database/sql"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type historyQuery struct {
	Sort string `form:"sort" binding:"omitempty,oneof=placed_at total status"`
	Dir  string `form:"dir" binding:"omitempty,oneof=asc desc"`
}

type HistoryAPI struct {
	DB *sql.DB
}

func (h *HistoryAPI) Orders(c *gin.Context) {
	var hq historyQuery
	if err := c.ShouldBindQuery(&hq); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if hq.Sort == "" {
		hq.Sort = "placed_at"
	}
	if hq.Dir == "" {
		hq.Dir = "desc"
	}

	customer := c.GetString("customer_id")
	q := fmt.Sprintf("SELECT id, total, status FROM orders WHERE customer_id = ? ORDER BY %s %s", hq.Sort, hq.Dir)
	rows, err := h.DB.Query(q, customer)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "history failed"})
		return
	}
	defer rows.Close()

	type row struct {
		ID     int64   `json:"id"`
		Total  float64 `json:"total"`
		Status string  `json:"status"`
	}
	var out []row
	for rows.Next() {
		var x row
		if rows.Scan(&x.ID, &x.Total, &x.Status) == nil {
			out = append(out, x)
		}
	}
	c.JSON(http.StatusOK, out)
}
