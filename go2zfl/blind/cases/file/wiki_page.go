package wiki

import (
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
)

const pagesDir = "/srv/wiki/pages"

func viewPage(w http.ResponseWriter, r *http.Request) {
	raw := r.FormValue("p")
	if strings.Contains(raw, "..") {
		http.Error(w, "invalid page", http.StatusBadRequest)
		return
	}
	title, err := url.QueryUnescape(raw)
	if err != nil {
		http.Error(w, "invalid encoding", http.StatusBadRequest)
		return
	}
	content, err := os.ReadFile(filepath.Join(pagesDir, title+".md"))
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "text/markdown; charset=utf-8")
	w.Write(content)
}

func init() {
	http.HandleFunc("/wiki/view", viewPage)
}
