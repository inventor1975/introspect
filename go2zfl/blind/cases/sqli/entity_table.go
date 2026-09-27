package entities

import (
	"database/sql"
	"fmt"
	"net/http"
)

type Kind int

const (
	KindUser Kind = iota
	KindTeam
	KindProject
)

func (k Kind) table() string {
	switch k {
	case KindTeam:
		return "teams"
	case KindProject:
		return "projects"
	default:
		return "users"
	}
}

func parseKind(s string) Kind {
	switch s {
	case "team":
		return KindTeam
	case "project":
		return KindProject
	}
	return KindUser
}

type EntityHandler struct {
	DB *sql.DB
}

func (h *EntityHandler) Name(w http.ResponseWriter, r *http.Request) {
	kind := parseKind(r.URL.Query().Get("kind"))
	id := r.URL.Query().Get("id")

	var name string
	q := fmt.Sprintf("SELECT name FROM %s WHERE id = $1", kind.table())
	if err := h.DB.QueryRow(q, id).Scan(&name); err != nil {
		http.NotFound(w, r)
		return
	}
	fmt.Fprintln(w, name)
}
