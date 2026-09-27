package comments

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"

	_ "github.com/go-sql-driver/mysql"
)

var conn *sql.DB

func Open(dsn string) error {
	var err error
	conn, err = sql.Open("mysql", dsn)
	return err
}

func escapeQuotes(s string) string {
	return strings.ReplaceAll(s, "'", "\\'")
}

type Comment struct {
	Author string `json:"author"`
	Text   string `json:"text"`
}

func CommentsByAuthor(w http.ResponseWriter, r *http.Request) {
	author := escapeQuotes(r.FormValue("author"))

	rows, err := conn.Query("SELECT author, body FROM comments WHERE author = '" + author + "' ORDER BY created_at DESC")
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	feed := make([]Comment, 0, 20)
	for rows.Next() {
		var c Comment
		rows.Scan(&c.Author, &c.Text)
		feed = append(feed, c)
	}
	json.NewEncoder(w).Encode(feed)
}
