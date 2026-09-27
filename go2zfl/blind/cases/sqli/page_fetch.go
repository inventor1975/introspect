package pages

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"
)

type Page struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
}

type PageHandler struct {
	DB *sql.DB
}

func (p *PageHandler) Get(w http.ResponseWriter, r *http.Request) {
	raw := r.URL.Query().Get("page_id")
	n, _ := strconv.Atoi(raw)
	if n < 0 {
		http.Error(w, "negative id", http.StatusBadRequest)
		return
	}

	var pg Page
	err := p.DB.QueryRow("SELECT id, title FROM pages WHERE id = " + raw).Scan(&pg.ID, &pg.Title)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	json.NewEncoder(w).Encode(pg)
}
