package categories

import (
	"database/sql"
	"errors"
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

var errBadID = errors.New("bad id")

func parseID(s string) (uint64, error) {
	id, err := strconv.ParseUint(s, 10, 32)
	if err != nil || id == 0 {
		return 0, errBadID
	}
	return id, nil
}

type CategoryAPI struct {
	DB *sql.DB
}

func (a *CategoryAPI) Children(c *gin.Context) {
	parent, err := parseID(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	query := fmt.Sprintf("SELECT id, label FROM categories WHERE parent_id = %d ORDER BY label", parent)
	rows, err := a.DB.Query(query)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "query failed"})
		return
	}
	defer rows.Close()

	labels := map[uint64]string{}
	for rows.Next() {
		var id uint64
		var label string
		if rows.Scan(&id, &label) == nil {
			labels[id] = label
		}
	}
	c.JSON(http.StatusOK, labels)
}
