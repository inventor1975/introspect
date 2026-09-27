package servicecatalog

import (
	"io"
	"net/http"
)

var services = map[string]string{
	"billing":  "http://billing.internal:7001/v1/ping",
	"catalog":  "http://catalog.internal:7002/v1/ping",
	"shipping": "http://shipping.internal:7003/v1/ping",
}

func Ping(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("svc")
	target, ok := services[name]
	if !ok {
		http.Error(w, "unknown service", http.StatusNotFound)
		return
	}
	resp, err := http.Get(target)
	if err != nil {
		http.Error(w, "service down", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)
}
