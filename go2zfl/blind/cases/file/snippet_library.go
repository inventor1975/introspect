package snippets

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

type Library struct {
	Root string
}

func (l *Library) Snippet(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("name")
	if name == "" || strings.Contains(name, "..") {
		http.Error(w, "invalid snippet name", http.StatusBadRequest)
		return
	}
	body, err := os.ReadFile(filepath.Join(l.Root, name))
	if err != nil {
		http.Error(w, "snippet not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.Write(body)
}

func Register(mux *http.ServeMux) {
	lib := &Library{Root: "/srv/snippets"}
	mux.HandleFunc("/snippets/raw", lib.Snippet)
}
