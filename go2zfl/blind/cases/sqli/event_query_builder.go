package events

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

type Event struct {
	Name  string `json:"name"`
	Venue string `json:"venue"`
	Day   string `json:"day"`
}

type EventsAPI struct {
	db *sql.DB
}

func (e *EventsAPI) Search(w http.ResponseWriter, r *http.Request) {
	city := mux.Vars(r)["city"]
	venue := r.URL.Query().Get("venue")

	var sb strings.Builder
	sb.WriteString("SELECT name, venue, day FROM events WHERE city = '")
	sb.WriteString(city)
	sb.WriteString("'")
	if venue != "" {
		sb.WriteString(" AND venue = '")
		sb.WriteString(venue)
		sb.WriteString("'")
	}
	sb.WriteString(" ORDER BY day")

	rows, err := e.db.Query(sb.String())
	if err != nil {
		http.Error(w, "search failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var list []Event
	for rows.Next() {
		var ev Event
		rows.Scan(&ev.Name, &ev.Venue, &ev.Day)
		list = append(list, ev)
	}
	json.NewEncoder(w).Encode(list)
}

func (e *EventsAPI) Attach(r *mux.Router) {
	r.HandleFunc("/cities/{city}/events", e.Search).Methods(http.MethodGet)
}
