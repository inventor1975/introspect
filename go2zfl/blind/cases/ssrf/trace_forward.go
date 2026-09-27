package traceforward

import (
	"io"
	"net/http"
	"time"
)

const ordersAPI = "http://orders.internal:9000/v1/orders"

var client = &http.Client{Timeout: 5 * time.Second}

func ListOrders(w http.ResponseWriter, r *http.Request) {
	req, err := http.NewRequestWithContext(r.Context(), http.MethodGet, ordersAPI, nil)
	if err != nil {
		http.Error(w, "internal error", http.StatusInternalServerError)
		return
	}
	req.Header.Set("X-Request-Id", r.Header.Get("X-Request-Id"))
	req.Header.Set("X-Upstream-Host", r.Header.Get("X-Upstream-Host"))
	req.Header.Set("Authorization", r.Header.Get("Authorization"))
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, "orders unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)
}
