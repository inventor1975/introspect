package notes

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

type Note struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
}

type NotesHandler struct {
	DB *sql.DB
}

func (h *NotesHandler) List(w http.ResponseWriter, r *http.Request) {
	owner := r.Header.Get("X-Owner")
	archived := r.URL.Query().Get("archived")
	pinned := r.URL.Query().Get("pinned")

	query := "SELECT id, title FROM notes WHERE owner = $1"
	if archived == "1" || archived == "true" {
		query += " AND archived = true"
	} else {
		query += " AND archived = false"
	}
	if pinned != "" {
		query += " AND pinned = true"
	}
	query += " ORDER BY updated_at DESC"

	rows, err := h.DB.Query(query, owner)
	if err != nil {
		http.Error(w, "list failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var notes []Note
	for rows.Next() {
		var n Note
		if rows.Scan(&n.ID, &n.Title) == nil {
			notes = append(notes, n)
		}
	}
	json.NewEncoder(w).Encode(notes)
}
