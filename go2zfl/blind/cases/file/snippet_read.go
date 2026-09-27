package snippets

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gorilla/mux"
)

var snippetRoot = "./snippets"

func stripTraversal(p string) string {
	return strings.ReplaceAll(p, "../", "")
}

func getSnippet(w http.ResponseWriter, r *http.Request) {
	name := stripTraversal(r.URL.Query().Get("name"))
	body, err := os.ReadFile(filepath.Join(snippetRoot, name))
	if err != nil {
		http.Error(w, "snippet not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/plain")
	w.Write(body)
}

func NewRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/snippets", getSnippet).Methods("GET")
	return r
}
