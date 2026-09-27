package bookmarks

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"

	_ "github.com/mattn/go-sqlite3"
)

func quoteLiteral(s string) string {
	return "'" + strings.ReplaceAll(s, "'", "''") + "'"
}

type BookmarkAPI struct {
	DB *sql.DB
}

func Open(path string) (*BookmarkAPI, error) {
	db, err := sql.Open("sqlite3", path)
	if err != nil {
		return nil, err
	}
	return &BookmarkAPI{DB: db}, nil
}

func (b *BookmarkAPI) ByTag(w http.ResponseWriter, r *http.Request) {
	tag := r.URL.Query().Get("tag")

	rows, err := b.DB.Query("SELECT url, title FROM bookmarks WHERE tag = " + quoteLiteral(tag) + " ORDER BY added DESC")
	if err != nil {
		http.Error(w, "query failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	type bm struct {
		URL   string `json:"url"`
		Title string `json:"title"`
	}
	var list []bm
	for rows.Next() {
		var x bm
		if rows.Scan(&x.URL, &x.Title) == nil {
			list = append(list, x)
		}
	}
	json.NewEncoder(w).Encode(list)
}
