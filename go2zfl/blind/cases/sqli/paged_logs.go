package logs

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type LogLine struct {
	At      time.Time `json:"at"`
	Level   string    `json:"level"`
	Message string    `json:"message"`
}

type LogViewer struct {
	DB *sql.DB
}

func (v *LogViewer) Page(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	limit := q.Get("limit")
	offset := q.Get("offset")
	if limit == "" {
		limit = "50"
	}
	if offset == "" {
		offset = "0"
	}

	ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second)
	defer cancel()

	query := fmt.Sprintf("SELECT at, level, message FROM app_logs ORDER BY at DESC LIMIT %s OFFSET %s", limit, offset)
	rows, err := v.DB.QueryContext(ctx, query)
	if err != nil {
		http.Error(w, "log query failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var out []LogLine
	for rows.Next() {
		var l LogLine
		if err := rows.Scan(&l.At, &l.Level, &l.Message); err != nil {
			continue
		}
		out = append(out, l)
	}
	json.NewEncoder(w).Encode(out)
}
