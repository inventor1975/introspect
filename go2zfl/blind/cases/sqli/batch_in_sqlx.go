package batch

import (
	"net/http"
	"strings"

	"github.com/jmoiron/sqlx"
)

type Doc struct {
	ID    string `db:"id" json:"id"`
	Title string `db:"title" json:"title"`
}

type DocsHandler struct {
	DB *sqlx.DB
}

func (h *DocsHandler) Many(w http.ResponseWriter, r *http.Request) {
	ids := strings.Split(r.URL.Query().Get("ids"), ",")

	query, args, err := sqlx.In("SELECT id, title FROM documents WHERE id IN (?)", ids)
	if err != nil {
		http.Error(w, "bad ids", http.StatusBadRequest)
		return
	}
	query = h.DB.Rebind(query)

	var docs []Doc
	if err := h.DB.Select(&docs, query, args...); err != nil {
		http.Error(w, "fetch failed", http.StatusInternalServerError)
		return
	}
	for _, d := range docs {
		w.Write([]byte(d.ID + "\n"))
	}
}
