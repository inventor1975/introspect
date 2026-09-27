package gallery

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
)

const pageSize = 24

type Gallery struct {
	DB *sql.DB
}

func (g *Gallery) Photos(w http.ResponseWriter, r *http.Request) {
	page, err := strconv.Atoi(r.URL.Query().Get("page"))
	if err != nil || page < 1 {
		page = 1
	}
	offset := (page - 1) * pageSize

	q := fmt.Sprintf("SELECT id, url FROM photos WHERE public = true ORDER BY id DESC LIMIT %d OFFSET %d", pageSize, offset)
	rows, err := g.DB.Query(q)
	if err != nil {
		http.Error(w, "gallery unavailable", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var urls []string
	for rows.Next() {
		var id int
		var u string
		if rows.Scan(&id, &u) == nil {
			urls = append(urls, u)
		}
	}
	json.NewEncoder(w).Encode(urls)
}
