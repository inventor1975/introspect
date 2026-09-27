package searchproxy

import (
	"io"
	"net/http"
	"net/url"

	"github.com/gorilla/mux"
)

const searchEndpoint = "https://search.internal.acme.io/v2/query"

func Search(w http.ResponseWriter, r *http.Request) {
	params := url.Values{}
	params.Set("q", r.URL.Query().Get("q"))
	params.Set("lang", r.URL.Query().Get("lang"))
	params.Set("limit", "25")
	resp, err := http.Get(searchEndpoint + "?" + params.Encode())
	if err != nil {
		http.Error(w, "search unavailable", http.StatusServiceUnavailable)
		return
	}
	defer resp.Body.Close()
	w.Header().Set("Content-Type", "application/json")
	io.Copy(w, resp.Body)
}

func Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/search", Search).Methods("GET")
	return r
}
