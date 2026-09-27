package tenants

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

type UserRow struct {
	ID    int64  `json:"id"`
	Email string `json:"email"`
}

type TenantAPI struct {
	DB *sql.DB
}

func (t *TenantAPI) Users(w http.ResponseWriter, r *http.Request) {
	tenant := r.Header.Get("X-Tenant-Schema")
	if tenant == "" {
		tenant = "public"
	}

	query := "SELECT id, email FROM " + tenant + ".users WHERE active = true ORDER BY id"
	rows, err := t.DB.QueryContext(r.Context(), query)
	if err != nil {
		http.Error(w, "unavailable", http.StatusServiceUnavailable)
		return
	}
	defer rows.Close()

	users := []UserRow{}
	for rows.Next() {
		var u UserRow
		if err := rows.Scan(&u.ID, &u.Email); err != nil {
			break
		}
		users = append(users, u)
	}
	json.NewEncoder(w).Encode(users)
}
