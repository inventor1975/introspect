package geocodeaddress

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
)

type location struct {
	Lat float64 `json:"lat"`
	Lng float64 `json:"lng"`
}

func Geocode(w http.ResponseWriter, r *http.Request) {
	address := r.FormValue("address")
	country := r.FormValue("country")
	endpoint := fmt.Sprintf("https://maps.geo-service.com/v1/geocode?address=%s&country=%s&key=%s",
		url.QueryEscape(address), url.QueryEscape(country), os.Getenv("GEO_KEY"))
	resp, err := http.Get(endpoint)
	if err != nil {
		http.Error(w, "geocoder unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var loc location
	if err := json.NewDecoder(resp.Body).Decode(&loc); err != nil {
		http.Error(w, "address not found", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(loc)
}
