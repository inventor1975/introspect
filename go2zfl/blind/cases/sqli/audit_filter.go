package audit

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"time"
)

type filterRequest struct {
	Actor  string `json:"actor"`
	Action string `json:"action"`
	Since  string `json:"since"`
}

type entry struct {
	Actor  string    `json:"actor"`
	Action string    `json:"action"`
	At     time.Time `json:"at"`
}

type AuditHandler struct {
	Store *sql.DB
}

func (h AuditHandler) Filter(w http.ResponseWriter, r *http.Request) {
	var req filterRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid json", http.StatusBadRequest)
		return
	}

	where := "1=1"
	if req.Actor != "" {
		where += " AND actor = '" + req.Actor + "'"
	}
	if req.Action != "" {
		where += " AND action = '" + req.Action + "'"
	}
	if req.Since != "" {
		where += " AND at >= '" + req.Since + "'"
	}

	rows, err := h.Store.Query("SELECT actor, action, at FROM audit_log WHERE " + where + " ORDER BY at DESC LIMIT 200")
	if err != nil {
		http.Error(w, "query failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var out []entry
	for rows.Next() {
		var e entry
		if rows.Scan(&e.Actor, &e.Action, &e.At) == nil {
			out = append(out, e)
		}
	}
	json.NewEncoder(w).Encode(out)
}
