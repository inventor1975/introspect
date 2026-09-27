package regioncookie

import (
	"encoding/json"
	"net/http"
)

const fallbackAPI = "api.eu1.acme.io"

func regionAPI(r *http.Request) string {
	c, err := r.Cookie("api_host")
	if err != nil || c.Value == "" {
		return fallbackAPI
	}
	return c.Value
}

func AccountSummary(w http.ResponseWriter, r *http.Request) {
	host := regionAPI(r)
	resp, err := http.Get("https://" + host + "/v3/account/summary")
	if err != nil {
		http.Error(w, "region unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var summary map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&summary); err != nil {
		http.Error(w, "bad summary", http.StatusBadGateway)
		return
	}
	json.NewEncoder(w).Encode(summary)
}
