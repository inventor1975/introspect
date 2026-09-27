package ratesoverride

import (
	"encoding/json"
	"net/http"
)

const ratesAPI = "https://api.exchange-feed.com/v2/latest"

type Rates struct {
	Base  string             `json:"base"`
	Rates map[string]float64 `json:"rates"`
}

func LatestRates(w http.ResponseWriter, r *http.Request) {
	source := ratesAPI
	if alt := r.FormValue("source"); alt != "" {
		source = alt
	}
	resp, err := http.Get(source + "?base=" + "EUR")
	if err != nil {
		http.Error(w, "rates unavailable", http.StatusServiceUnavailable)
		return
	}
	defer resp.Body.Close()
	var out Rates
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil {
		http.Error(w, "bad upstream payload", http.StatusBadGateway)
		return
	}
	json.NewEncoder(w).Encode(out)
}
