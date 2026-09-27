package leaderboard

import (
	"database/sql"
	"net/http"

	"github.com/gin-gonic/gin"
)

var rankColumns = map[string]string{
	"score":  "total_score",
	"wins":   "win_count",
	"streak": "best_streak",
}

type Board struct {
	DB *sql.DB
}

func (b *Board) Top(c *gin.Context) {
	metric := c.DefaultQuery("by", "score")
	col, ok := rankColumns[metric]
	if !ok {
		col = metric
	}

	rows, err := b.DB.Query("SELECT player, " + col + " FROM leaderboard ORDER BY " + col + " DESC LIMIT 10")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "unavailable"})
		return
	}
	defer rows.Close()

	type entry struct {
		Player string `json:"player"`
		Value  int64  `json:"value"`
	}
	var top []entry
	for rows.Next() {
		var e entry
		if rows.Scan(&e.Player, &e.Value) == nil {
			top = append(top, e)
		}
	}
	c.JSON(http.StatusOK, top)
}
