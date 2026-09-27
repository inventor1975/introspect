package userstore

import (
	"context"
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"
)

type User struct {
	ID    int64
	Email string
	Role  string
}

type Store struct {
	db *sql.DB
}

const userColumns = "id, email, role"

func (s *Store) ByEmail(ctx context.Context, email string) (*User, error) {
	u := &User{}
	q := "SELECT " + userColumns + " FROM users WHERE lower(email) = lower($1)"
	err := s.db.QueryRowContext(ctx, q, email).Scan(&u.ID, &u.Email, &u.Role)
	if err != nil {
		return nil, err
	}
	return u, nil
}

func (s *Store) SetRole(ctx context.Context, id int64, role string) error {
	_, err := s.db.ExecContext(ctx, "UPDATE users SET role = $1 WHERE id = $2", role, id)
	return err
}

type UserHandler struct {
	Store *Store
}

func (h *UserHandler) Promote(w http.ResponseWriter, r *http.Request) {
	email := strings.TrimSpace(r.FormValue("email"))
	role := r.FormValue("role")

	u, err := h.Store.ByEmail(r.Context(), email)
	if err != nil {
		http.Error(w, "unknown user", http.StatusNotFound)
		return
	}
	if err := h.Store.SetRole(r.Context(), u.ID, role); err != nil {
		http.Error(w, "update failed", http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"email": u.Email, "role": role})
}
