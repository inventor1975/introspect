package shadowedtarget

import (
	"encoding/json"
	"log"
	"net/http"
)

func Weather(w http.ResponseWriter, r *http.Request) {
	target := "https://weather.acme.io/v1/current?city=berlin"
	if r.URL.Query().Has("target") {
		target := r.URL.Query().Get("target")
		log.Printf("weather: client suggested target %s", target)
	}
	resp, err := http.Get(target)
	if err != nil {
		http.Error(w, "weather unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var data map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&data)
	json.NewEncoder(w).Encode(data)
}
