package thumbs

import (
	"net/http"
	"os"
	"path/filepath"
)

const thumbDir = "/var/cache/thumbs"

func thumbnail(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	id := filepath.Base(q.Get("id"))
	ext := q.Get("ext")
	if ext == "" {
		ext = ".webp"
	}
	b, err := os.ReadFile(filepath.Join(thumbDir, id+ext))
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "image/webp")
	w.Write(b)
}

func init() {
	http.HandleFunc("/thumb", thumbnail)
}
