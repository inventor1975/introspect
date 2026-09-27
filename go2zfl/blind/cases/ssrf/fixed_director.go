package main

import (
	"log"
	"net/http"
	"net/http/httputil"
)

const reportsBackend = "reports.internal:9400"

func reportsProxy() *httputil.ReverseProxy {
	return &httputil.ReverseProxy{
		Director: func(req *http.Request) {
			if fh := req.Header.Get("X-Forwarded-Host"); fh != "" {
				log.Printf("reports proxy: request originally for %s", fh)
			}
			req.URL.Scheme = "http"
			req.URL.Host = reportsBackend
			req.Host = reportsBackend
		},
	}
}

func main() {
	http.Handle("/reports/", reportsProxy())
	log.Fatal(http.ListenAndServe(":8090", nil))
}
