package exports

import (
	"net/http"
	"path/filepath"
)

type ExportServer struct {
	Base string
}

func (s *ExportServer) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("name")
	if name == "" {
		http.Error(w, "name required", http.StatusBadRequest)
		return
	}
	rooted := filepath.Clean("/" + name)
	http.ServeFile(w, r, filepath.Join(s.Base, rooted))
}

func main() {
	http.Handle("/exports/bundle", &ExportServer{Base: "/var/exports/bundles"})
	http.ListenAndServe(":8080", nil)
}
