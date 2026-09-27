package projects

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
)

type ctxKey string

const tenantKey ctxKey = "tenant_id"

type ProjectAPI struct {
	DB *sql.DB
}

func (p *ProjectAPI) List(w http.ResponseWriter, r *http.Request) {
	tenantID, ok := r.Context().Value(tenantKey).(int64)
	if !ok {
		http.Error(w, "no tenant", http.StatusUnauthorized)
		return
	}
	name := r.URL.Query().Get("name")

	q := fmt.Sprintf("SELECT id, name FROM tenant_%d.projects WHERE name ILIKE $1", tenantID)
	rows, err := p.DB.Query(q, "%"+name+"%")
	if err != nil {
		http.Error(w, "list failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	out := map[int64]string{}
	for rows.Next() {
		var id int64
		var n string
		if rows.Scan(&id, &n) == nil {
			out[id] = n
		}
	}
	json.NewEncoder(w).Encode(out)
}
