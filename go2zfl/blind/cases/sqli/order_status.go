package orderstatus

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

var db *sql.DB

type statusResponse struct {
	ID     string `json:"id"`
	Status string `json:"status"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	if id == "" {
		http.Error(w, "missing id", http.StatusBadRequest)
		return
	}

	var resp statusResponse
	query := "SELECT id, status FROM orders WHERE id = $1"
	if err := db.QueryRow(query, id).Scan(&resp.ID, &resp.Status); err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(resp)
}

func Register(mux *http.ServeMux, conn *sql.DB) {
	db = conn
	mux.HandleFunc("/orders/status", statusHandler)
}
