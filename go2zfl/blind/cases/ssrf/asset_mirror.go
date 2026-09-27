package assetmirror

import (
	"io"
	"log"
	"net/http"

	"github.com/gorilla/mux"

	"example.com/blindsvc/lib/allow"
)

func Mirror(w http.ResponseWriter, r *http.Request) {
	raw := r.URL.Query().Get("asset")
	if _, err := allow.Check(raw); err != nil {
		log.Printf("mirror: asset %q outside trusted hosts: %v", raw, err)
	}
	resp, err := http.Get(raw)
	if err != nil {
		http.Error(w, "asset unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
	io.Copy(w, resp.Body)
}

func Routes(r *mux.Router) {
	r.HandleFunc("/assets/mirror", Mirror)
}
