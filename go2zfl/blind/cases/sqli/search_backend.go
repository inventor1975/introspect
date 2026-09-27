package search

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"os"
)

type Searcher interface {
	Search(db *sql.DB, term string) (*sql.Rows, error)
}

type postgresSearch struct{}

func (postgresSearch) Search(db *sql.DB, term string) (*sql.Rows, error) {
	return db.Query("SELECT id, title FROM docs WHERE to_tsvector(body) @@ plainto_tsquery('" + term + "')")
}

type likeSearch struct{}

func (likeSearch) Search(db *sql.DB, term string) (*sql.Rows, error) {
	return db.Query("SELECT id, title FROM docs WHERE body LIKE '%" + term + "%'")
}

var registry = map[string]Searcher{
	"fts":  postgresSearch{},
	"like": likeSearch{},
}

var active Searcher

func init() {
	if s, ok := registry[os.Getenv("SEARCH_BACKEND")]; ok {
		active = s
	} else {
		active = likeSearch{}
	}
}

type SearchHandler struct {
	DB *sql.DB
}

func (h *SearchHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	rows, err := active.Search(h.DB, r.FormValue("q"))
	if err != nil {
		http.Error(w, "search error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var titles []string
	for rows.Next() {
		var id int
		var title string
		if rows.Scan(&id, &title) == nil {
			titles = append(titles, title)
		}
	}
	json.NewEncoder(w).Encode(titles)
}
