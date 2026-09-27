package site

import (
	"log"
	"net/http"
	"path/filepath"
	"strings"
)

const publicDir = "/srv/www/public"

func serveSite(w http.ResponseWriter, r *http.Request) {
	if strings.HasPrefix(r.URL.Path, "/.well-known/") {
		w.Header().Set("Cache-Control", "no-store")
	}
	w.Header().Set("X-Content-Type-Options", "nosniff")
	http.ServeFile(w, r, filepath.Join(publicDir, r.URL.Path))
}

func main() {
	http.HandleFunc("/", serveSite)
	log.Fatal(http.ListenAndServe(":80", nil))
}
