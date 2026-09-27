package threads

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"
)

type ThreadList struct {
	DB *sql.DB
}

func (t *ThreadList) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	dir := r.URL.Query().Get("dir")
	board := r.URL.Query().Get("board")

	var order string
	switch strings.ToLower(dir) {
	case "asc":
		order = "ASC"
	case "desc", "":
		order = "DESC"
	default:
		http.Error(w, "dir must be asc or desc", http.StatusBadRequest)
		return
	}

	rows, err := t.DB.Query("SELECT id, title FROM threads WHERE board = $1 ORDER BY last_post_at "+order, board)
	if err != nil {
		http.Error(w, "failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	titles := map[int]string{}
	for rows.Next() {
		var id int
		var title string
		if rows.Scan(&id, &title) == nil {
			titles[id] = title
		}
	}
	json.NewEncoder(w).Encode(titles)
}
