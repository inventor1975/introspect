package metrics

import (
	"database/sql"
	"net/http"
	"regexp"

	"github.com/gin-gonic/gin"
)

var identRe = regexp.MustCompile(`^[a-z][a-z0-9_]{0,30}$`)

type MetricsAPI struct {
	DB *sql.DB
}

func (m *MetricsAPI) Sum(c *gin.Context) {
	column := c.Param("column")
	if !identRe.MatchString(column) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid column"})
		return
	}

	var total float64
	err := m.DB.QueryRow("SELECT COALESCE(SUM("+column+"), 0) FROM daily_metrics WHERE day >= ?", c.Query("from")).Scan(&total)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "sum failed"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"column": column, "total": total})
}
