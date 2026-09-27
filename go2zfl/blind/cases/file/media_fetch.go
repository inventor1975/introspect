package media

import (
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
)

type Library struct {
	Root string
}

func (l *Library) fetch(w http.ResponseWriter, r *http.Request) {
	name := r.PathValue("name")
	f, err := os.Open(filepath.Join(l.Root, "tracks", name))
	if err != nil {
		http.NotFound(w, r)
		return
	}
	defer f.Close()
	w.Header().Set("Content-Type", "audio/mpeg")
	if _, err := io.Copy(w, f); err != nil {
		log.Printf("stream %s: %v", name, err)
	}
}

func main() {
	lib := &Library{Root: "/srv/media"}
	mux := http.NewServeMux()
	mux.HandleFunc("GET /media/{name}", lib.fetch)
	log.Fatal(http.ListenAndServe(":8090", mux))
}
