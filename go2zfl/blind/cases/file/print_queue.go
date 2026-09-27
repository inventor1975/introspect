package printing

import (
	"errors"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

var allowedSpoolExt = map[string]bool{".pdf": true, ".ps": true, ".pcl": true}

type Spooler struct {
	dir string
}

func (s *Spooler) jobPath(name string) (string, error) {
	base := filepath.Base(name)
	if base == "." || base == ".." || base == "/" {
		return "", errors.New("invalid job name")
	}
	if !allowedSpoolExt[strings.ToLower(filepath.Ext(base))] {
		return "", errors.New("unsupported job type")
	}
	return filepath.Join(s.dir, base), nil
}

func (s *Spooler) Submit(w http.ResponseWriter, r *http.Request) {
	path, err := s.jobPath(r.FormValue("job"))
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	src, _, err := r.FormFile("document")
	if err != nil {
		http.Error(w, "document required", http.StatusBadRequest)
		return
	}
	defer src.Close()
	out, err := os.OpenFile(path, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0o640)
	if err != nil {
		http.Error(w, "job already queued", http.StatusConflict)
		return
	}
	defer out.Close()
	io.Copy(out, src)
	w.WriteHeader(http.StatusAccepted)
}

func Register(mux *http.ServeMux) {
	s := &Spooler{dir: "/var/spool/portal"}
	mux.HandleFunc("/print/submit", s.Submit)
}
