package usage

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
)

var usageTables = []string{"api_calls", "storage_events", "compute_minutes"}

type UsageAPI struct {
	DB *sql.DB
}

func (u *UsageAPI) Summary(w http.ResponseWriter, r *http.Request) {
	account := r.URL.Query().Get("account")
	since := r.URL.Query().Get("since")

	summary := make(map[string]int64, len(usageTables))
	for _, tbl := range usageTables {
		var n int64
		q := fmt.Sprintf("SELECT COUNT(*) FROM %s WHERE account_id = $1 AND created_at >= $2", tbl)
		if err := u.DB.QueryRow(q, account, since).Scan(&n); err != nil {
			http.Error(w, "summary failed", http.StatusInternalServerError)
			return
		}
		summary[tbl] = n
	}
	json.NewEncoder(w).Encode(summary)
}
