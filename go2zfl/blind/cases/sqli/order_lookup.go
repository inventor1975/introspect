package orderlookup

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

var db *sql.DB

type order struct {
	ID     int64   `json:"id"`
	Status string  `json:"status"`
	Total  float64 `json:"total"`
}

func orderHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	if id == "" {
		http.Error(w, "missing id", http.StatusBadRequest)
		return
	}

	rows, err := db.Query("SELECT id, status, total FROM orders WHERE id = " + id)
	if err != nil {
		http.Error(w, "query failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var out []order
	for rows.Next() {
		var o order
		if err := rows.Scan(&o.ID, &o.Status, &o.Total); err != nil {
			continue
		}
		out = append(out, o)
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(out)
}

func Register(mux *http.ServeMux, conn *sql.DB) {
	db = conn
	mux.HandleFunc("/orders", orderHandler)
}
