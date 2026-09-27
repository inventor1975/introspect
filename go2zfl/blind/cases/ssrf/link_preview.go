package linkpreview

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"regexp"

	"github.com/gorilla/mux"
)

var titleRe = regexp.MustCompile(`(?is)<title>(.*?)</title>`)

func Preview(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	site := vars["site"]
	page := fmt.Sprintf("https://%s/", site)
	resp, err := http.Get(page)
	if err != nil {
		http.Error(w, "unreachable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	html, _ := io.ReadAll(io.LimitReader(resp.Body, 512*1024))
	title := ""
	if m := titleRe.FindSubmatch(html); m != nil {
		title = string(m[1])
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"site": site, "title": title})
}

func NewRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/preview/{site}", Preview).Methods("GET")
	return r
}
