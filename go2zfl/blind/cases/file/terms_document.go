package legal

import (
	"net/http"
	"os"
	"path/filepath"
)

const legalDir = "/srv/site/legal"

var documents = map[string]string{
	"tos":     "terms-of-service.html",
	"privacy": "privacy-policy.html",
	"cookies": "cookie-policy.html",
	"imprint": "imprint.html",
	"dpa":     "data-processing-agreement.html",
}

func legalDocument(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("doc")
	file, ok := documents[key]
	if !ok {
		http.NotFound(w, r)
		return
	}
	html, err := os.ReadFile(filepath.Join(legalDir, file))
	if err != nil {
		http.Error(w, "document unavailable", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write(html)
}

func init() {
	http.HandleFunc("/legal", legalDocument)
}
