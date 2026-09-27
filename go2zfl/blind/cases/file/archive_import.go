package importer

import (
	"archive/zip"
	"bytes"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

const stagingDir = "/var/lib/importer/staging"

func ImportArchive(w http.ResponseWriter, r *http.Request) {
	file, _, err := r.FormFile("archive")
	if err != nil {
		http.Error(w, "archive required", http.StatusBadRequest)
		return
	}
	defer file.Close()
	buf, err := io.ReadAll(io.LimitReader(file, 50<<20))
	if err != nil {
		http.Error(w, "read error", http.StatusBadRequest)
		return
	}
	zr, err := zip.NewReader(bytes.NewReader(buf), int64(len(buf)))
	if err != nil {
		http.Error(w, "not a zip file", http.StatusBadRequest)
		return
	}
	for _, zf := range zr.File {
		target := filepath.Join(stagingDir, zf.Name)
		if zf.FileInfo().IsDir() {
			os.MkdirAll(target, 0o755)
			continue
		}
		if err := os.MkdirAll(filepath.Dir(target), 0o755); err != nil {
			http.Error(w, "mkdir failed", http.StatusInternalServerError)
			return
		}
		rc, err := zf.Open()
		if err != nil {
			continue
		}
		out, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, zf.Mode())
		if err != nil {
			rc.Close()
			continue
		}
		io.Copy(out, rc)
		out.Close()
		rc.Close()
	}
	w.WriteHeader(http.StatusAccepted)
}
