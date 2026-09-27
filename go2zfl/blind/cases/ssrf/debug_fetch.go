package debugfetch

import (
	"encoding/json"
	"net/http"
)

const allowCustomEndpoint = false

const defaultPricing = "https://pricing.internal.acme.io/v1/plans"

func Plans(w http.ResponseWriter, r *http.Request) {
	endpoint := defaultPricing
	if allowCustomEndpoint {
		if e := r.URL.Query().Get("endpoint"); e != "" {
			endpoint = e
		}
	}
	resp, err := http.Get(endpoint)
	if err != nil {
		http.Error(w, "pricing unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var plans []map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&plans)
	json.NewEncoder(w).Encode(plans)
}
