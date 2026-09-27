package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"
)

const legacyBackend = "http://legacy-app.internal:8081"

func legacyHandler() http.Handler {
	target, err := url.Parse(legacyBackend)
	if err != nil {
		log.Fatal(err)
	}
	proxy := httputil.NewSingleHostReverseProxy(target)
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		r.URL.Path = strings.TrimPrefix(r.URL.Path, "/legacy")
		r.Header.Set("X-Forwarded-Prefix", "/legacy")
		proxy.ServeHTTP(w, r)
	})
}

func main() {
	http.Handle("/legacy/", legacyHandler())
	log.Fatal(http.ListenAndServe(":8080", nil))
}
