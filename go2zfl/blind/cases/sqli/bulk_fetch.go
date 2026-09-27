package bulk

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"
)

type Record struct {
	ID    string `json:"id"`
	Title string `json:"title"`
}

var DB *sql.DB

func FetchMany(w http.ResponseWriter, r *http.Request) {
	ids := r.URL.Query()["id"]
	if len(ids) == 0 {
		w.Write([]byte("[]"))
		return
	}

	quoted := make([]string, 0, len(ids))
	for _, id := range ids {
		id = strings.TrimSpace(id)
		if id == "" {
			continue
		}
		quoted = append(quoted, "'"+id+"'")
	}

	query := "SELECT id, title FROM documents WHERE id IN (" + strings.Join(quoted, ",") + ")"
	rows, err := DB.Query(query)
	if err != nil {
		http.Error(w, "fetch failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var recs []Record
	for rows.Next() {
		var rec Record
		rows.Scan(&rec.ID, &rec.Title)
		recs = append(recs, rec)
	}
	json.NewEncoder(w).Encode(recs)
}
