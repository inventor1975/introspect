package schemeguard

import (
	"io"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

func FetchDocument(w http.ResponseWriter, r *http.Request) {
	docURL := r.URL.Query().Get("doc")
	if !strings.HasPrefix(docURL, "https://") {
		http.Error(w, "only https documents are supported", http.StatusBadRequest)
		return
	}
	resp, err := http.Get(docURL)
	if err != nil {
		http.Error(w, "fetch failed", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	io.Copy(w, io.LimitReader(resp.Body, 1<<20))
}

func Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/docs/fetch", FetchDocument).Methods(http.MethodGet)
	return r
}
