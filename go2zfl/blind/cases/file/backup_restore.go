package admin

import (
	"archive/tar"
	"compress/gzip"
	"io"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gorilla/mux"
)

type RestoreHandler struct {
	DataDir string
}

func (h *RestoreHandler) Restore(w http.ResponseWriter, r *http.Request) {
	gz, err := gzip.NewReader(r.Body)
	if err != nil {
		http.Error(w, "expected .tar.gz body", http.StatusBadRequest)
		return
	}
	defer gz.Close()
	tr := tar.NewReader(gz)
	restored := 0
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			http.Error(w, "corrupt archive", http.StatusBadRequest)
			return
		}
		dest := filepath.Join(h.DataDir, hdr.Name)
		switch hdr.Typeflag {
		case tar.TypeDir:
			os.MkdirAll(dest, os.FileMode(hdr.Mode))
		case tar.TypeReg:
			f, err := os.Create(dest)
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			io.Copy(f, tr)
			f.Close()
			restored++
		}
	}
	w.WriteHeader(http.StatusNoContent)
}

func Routes(h *RestoreHandler) *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/admin/restore", h.Restore).Methods("POST")
	return r
}
