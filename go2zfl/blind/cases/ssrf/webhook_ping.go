package webhookping

import (
	"bytes"
	"encoding/json"
	"net/http"
	"time"
)

type pingPayload struct {
	Event  string    `json:"event"`
	SentAt time.Time `json:"sent_at"`
}

func TestDelivery(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
	callback := r.FormValue("callback")
	body, _ := json.Marshal(pingPayload{Event: "ping", SentAt: time.Now().UTC()})
	resp, err := http.Post(callback, "application/json", bytes.NewReader(body))
	if err != nil {
		w.WriteHeader(http.StatusBadGateway)
		json.NewEncoder(w).Encode(map[string]string{"error": err.Error()})
		return
	}
	defer resp.Body.Close()
	json.NewEncoder(w).Encode(map[string]int{"status": resp.StatusCode})
}
