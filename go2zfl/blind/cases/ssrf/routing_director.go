package main

import (
	"log"
	"net/http"
	"net/http/httputil"
)

func NewTenantProxy() http.Handler {
	return &httputil.ReverseProxy{
		Director: func(req *http.Request) {
			tenantHost := req.Header.Get("X-Tenant-Backend")
			if tenantHost == "" {
				tenantHost = "shared-pool.internal:9000"
			}
			req.URL.Scheme = "http"
			req.URL.Host = tenantHost
			req.Host = tenantHost
			req.Header.Del("X-Tenant-Backend")
		},
		ErrorLog: log.Default(),
	}
}

func main() {
	http.Handle("/api/", NewTenantProxy())
	log.Fatal(http.ListenAndServe(":8443", nil))
}
