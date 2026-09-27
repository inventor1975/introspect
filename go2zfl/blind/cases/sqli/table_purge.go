package admin

import (
	"database/sql"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

type Maintenance struct {
	DB *sql.DB
}

func (m *Maintenance) PurgeOld(c *gin.Context) {
	table := c.Param("table")
	days := c.DefaultQuery("days", "90")

	query := "DELETE FROM " + table + " WHERE created_at < NOW() - INTERVAL '" + days + " days'"
	res, err := m.DB.ExecContext(c.Request.Context(), query)
	if err != nil {
		log.Printf("purge %s: %v", table, err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "purge failed"})
		return
	}
	n, _ := res.RowsAffected()
	c.JSON(http.StatusOK, gin.H{"deleted": n})
}

func (m *Maintenance) Mount(r *gin.Engine) {
	g := r.Group("/admin")
	g.POST("/purge/:table", m.PurgeOld)
}
