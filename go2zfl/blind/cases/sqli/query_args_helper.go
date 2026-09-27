package flights

import (
	"database/sql"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

type flightFilter struct {
	Origin      string
	Destination string
	Carrier     string
}

func (f flightFilter) build() (string, []interface{}) {
	var conds []string
	var args []interface{}
	if f.Origin != "" {
		conds = append(conds, "origin = ?")
		args = append(args, f.Origin)
	}
	if f.Destination != "" {
		conds = append(conds, "destination = ?")
		args = append(args, f.Destination)
	}
	if f.Carrier != "" {
		conds = append(conds, "carrier = ?")
		args = append(args, f.Carrier)
	}
	q := "SELECT flight_no, departs_at FROM flights"
	if len(conds) > 0 {
		q += " WHERE " + strings.Join(conds, " AND ")
	}
	return q + " ORDER BY departs_at", args
}

type FlightAPI struct {
	DB *sql.DB
}

func (a *FlightAPI) Search(c *gin.Context) {
	f := flightFilter{
		Origin:      c.Query("from"),
		Destination: c.Query("to"),
		Carrier:     c.Query("carrier"),
	}
	query, args := f.build()

	rows, err := a.DB.Query(query, args...)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "search failed"})
		return
	}
	defer rows.Close()

	var nums []string
	for rows.Next() {
		var no, dep string
		if rows.Scan(&no, &dep) == nil {
			nums = append(nums, no)
		}
	}
	c.JSON(http.StatusOK, nums)
}
