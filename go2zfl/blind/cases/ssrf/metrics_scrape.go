package metricsscrape

import (
	"fmt"
	"io"
	"net/http"
	"strconv"
)

var exporterPorts = map[int]string{
	9100: "node",
	9187: "postgres",
	9121: "redis",
}

func Scrape(w http.ResponseWriter, r *http.Request) {
	port, err := strconv.Atoi(r.FormValue("port"))
	if err != nil {
		http.Error(w, "port must be numeric", http.StatusBadRequest)
		return
	}
	if _, known := exporterPorts[port]; !known {
		http.Error(w, "unknown exporter", http.StatusBadRequest)
		return
	}
	resp, err := http.Get(fmt.Sprintf("http://127.0.0.1:%d/metrics", port))
	if err != nil {
		http.Error(w, "exporter down", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.Header().Set("Content-Type", "text/plain; version=0.0.4")
	io.Copy(w, resp.Body)
}
