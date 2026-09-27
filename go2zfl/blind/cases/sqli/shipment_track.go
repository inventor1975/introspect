package shipping

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"regexp"
)

var trackingPattern = regexp.MustCompile(`[A-Z]{2}[0-9]{9}`)

type Tracker struct {
	DB *sql.DB
}

type status struct {
	Code     string `json:"code"`
	Location string `json:"location"`
	Stage    string `json:"stage"`
}

func (t *Tracker) Track(w http.ResponseWriter, r *http.Request) {
	code := r.URL.Query().Get("tracking")
	if !trackingPattern.MatchString(code) {
		http.Error(w, "malformed tracking number", http.StatusBadRequest)
		return
	}

	var st status
	err := t.DB.QueryRow("SELECT code, location, stage FROM shipments WHERE code = '"+code+"'").
		Scan(&st.Code, &st.Location, &st.Stage)
	if err != nil {
		http.Error(w, "unknown shipment", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(st)
}
