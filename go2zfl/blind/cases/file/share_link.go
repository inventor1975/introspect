package share

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gorilla/mux"
)

type Share struct {
	Dir string
}

func (s *Share) open(w http.ResponseWriter, r *http.Request) {
	rel := mux.Vars(r)["path"]
	full := filepath.Join(s.Dir, rel)
	f, err := os.Open(full)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	defer f.Close()
	st, err := f.Stat()
	if err != nil || st.IsDir() {
		http.NotFound(w, r)
		return
	}
	http.ServeContent(w, r, st.Name(), st.ModTime(), f)
}

func NewRouter(s *Share) *mux.Router {
	r := mux.NewRouter().SkipClean(true)
	r.HandleFunc("/s/{path:.*}", s.open).Methods(http.MethodGet)
	return r
}
