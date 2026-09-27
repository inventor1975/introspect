package glossary

import (
	"net/http"
	"net/url"
	"os"
	"path/filepath"
)

const entriesDir = "/srv/glossary/entries"

func entry(w http.ResponseWriter, r *http.Request) {
	term := r.URL.Query().Get("term")
	if term == "" {
		http.Error(w, "term required", http.StatusBadRequest)
		return
	}
	fname := url.PathEscape(term) + ".json"
	data, err := os.ReadFile(filepath.Join(entriesDir, fname))
	if err != nil {
		http.Error(w, "no glossary entry", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(data)
}

func init() {
	http.HandleFunc("/glossary", entry)
}
