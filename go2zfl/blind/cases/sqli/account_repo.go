package accounts

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"
)

type Account struct {
	ID    int64
	Email string
	Plan  string
}

type AccountRepository struct {
	db *sql.DB
}

func NewAccountRepository(db *sql.DB) *AccountRepository {
	return &AccountRepository{db: db}
}

func (r *AccountRepository) FindByEmail(email string) (*Account, error) {
	a := &Account{}
	q := "SELECT id, email, plan FROM accounts WHERE lower(email) = '" + strings.ToLower(email) + "'"
	if err := r.db.QueryRow(q).Scan(&a.ID, &a.Email, &a.Plan); err != nil {
		return nil, err
	}
	return a, nil
}

type AccountHandler struct {
	Repo *AccountRepository
}

func (h *AccountHandler) Lookup(w http.ResponseWriter, r *http.Request) {
	email := strings.TrimSpace(r.FormValue("email"))
	acct, err := h.Repo.FindByEmail(email)
	if err != nil {
		http.Error(w, "no such account", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"id": acct.ID, "plan": acct.Plan})
}
