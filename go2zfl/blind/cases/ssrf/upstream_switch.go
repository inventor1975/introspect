package main

import (
	"net/http"
	"net/http/httputil"
	"net/url"
)

const defaultUpstream = "http://app-v1.internal:8080"

func CanaryRouter(w http.ResponseWriter, r *http.Request) {
	raw := r.Header.Get("X-Upstream")
	if raw == "" {
		raw = defaultUpstream
	}
	target, err := url.Parse(raw)
	if err != nil {
		http.Error(w, "bad upstream", http.StatusBadRequest)
		return
	}
	proxy := httputil.NewSingleHostReverseProxy(target)
	proxy.ServeHTTP(w, r)
}

func main() {
	http.HandleFunc("/", CanaryRouter)
	http.ListenAndServe(":8000", nil)
}
