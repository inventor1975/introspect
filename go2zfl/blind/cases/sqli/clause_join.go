package bookings

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"
)

func and(parts ...string) string {
	kept := parts[:0]
	for _, p := range parts {
		if p != "" {
			kept = append(kept, p)
		}
	}
	if len(kept) == 0 {
		return "TRUE"
	}
	return strings.Join(kept, " AND ")
}

func eq(col, val string) string {
	if val == "" {
		return ""
	}
	return col + " = '" + val + "'"
}

type BookingHandler struct {
	DB *sql.DB
}

func (b *BookingHandler) Search(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	where := and(eq("room", q.Get("room")), eq("guest_name", q.Get("guest")), "cancelled = false")

	rows, err := b.DB.Query("SELECT id, room, guest_name FROM bookings WHERE " + where)
	if err != nil {
		http.Error(w, "failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	type booking struct {
		ID    int    `json:"id"`
		Room  string `json:"room"`
		Guest string `json:"guest"`
	}
	var out []booking
	for rows.Next() {
		var bk booking
		rows.Scan(&bk.ID, &bk.Room, &bk.Guest)
		out = append(out, bk)
	}
	json.NewEncoder(w).Encode(out)
}
