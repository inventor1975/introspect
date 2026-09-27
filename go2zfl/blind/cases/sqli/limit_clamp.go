package feed

import (
	"database/sql"
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

const (
	defaultLimit = 20
	maxLimit     = 100
)

type FeedAPI struct {
	DB *sql.DB
}

func (f *FeedAPI) Latest(c *gin.Context) {
	limit := defaultLimit
	if v := c.Query("limit"); v != "" {
		n, err := strconv.Atoi(v)
		if err == nil && n > 0 && n <= maxLimit {
			limit = n
		}
	}

	q := fmt.Sprintf("SELECT id, headline FROM posts WHERE published = 1 ORDER BY published_at DESC LIMIT %d", limit)
	rows, err := f.DB.Query(q)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "feed failed"})
		return
	}
	defer rows.Close()

	type item struct {
		ID       int    `json:"id"`
		Headline string `json:"headline"`
	}
	var items []item
	for rows.Next() {
		var it item
		if rows.Scan(&it.ID, &it.Headline) == nil {
			items = append(items, it)
		}
	}
	c.JSON(http.StatusOK, items)
}
