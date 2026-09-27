package reportcols

import (
	"database/sql"
	"net/http"

	"github.com/gin-gonic/gin"
)

var sortable = map[string]string{
	"date":    "created_at",
	"amount":  "amount",
	"region":  "region_code",
	"product": "product_name",
}

type ReportAPI struct {
	DB *sql.DB
}

func (r *ReportAPI) Rows(c *gin.Context) {
	key := c.DefaultQuery("sort", "date")
	col, ok := sortable[key]
	if !ok {
		col = "created_at"
	}

	rows, err := r.DB.Query("SELECT id, region_code, amount FROM sales ORDER BY " + col + " DESC LIMIT 500")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "query failed"})
		return
	}
	defer rows.Close()

	type row struct {
		ID     int     `json:"id"`
		Region string  `json:"region"`
		Amount float64 `json:"amount"`
	}
	var out []row
	for rows.Next() {
		var x row
		if rows.Scan(&x.ID, &x.Region, &x.Amount) == nil {
			out = append(out, x)
		}
	}
	c.JSON(http.StatusOK, out)
}
