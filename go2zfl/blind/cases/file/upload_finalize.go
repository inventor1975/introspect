package uploads

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

const (
	pendingDir = "/var/uploads/pending"
	libraryDir = "/var/uploads/library"
)

func sanitizeFilename(raw string) string {
	cleaned := strings.Map(func(r rune) rune {
		switch {
		case r >= 'a' && r <= 'z', r >= 'A' && r <= 'Z', r >= '0' && r <= '9':
			return r
		case r == '.', r == '-', r == '_':
			return r
		}
		return -1
	}, raw)
	cleaned = strings.TrimLeft(cleaned, ".")
	if len(cleaned) > 120 {
		cleaned = cleaned[:120]
	}
	return cleaned
}

func finalize(w http.ResponseWriter, r *http.Request) {
	tmp := sanitizeFilename(r.PostFormValue("upload_id"))
	name := sanitizeFilename(r.PostFormValue("filename"))
	if tmp == "" || name == "" {
		http.Error(w, "invalid name", http.StatusBadRequest)
		return
	}
	if err := os.Rename(filepath.Join(pendingDir, tmp), filepath.Join(libraryDir, name)); err != nil {
		http.Error(w, "finalize failed", http.StatusInternalServerError)
		return
	}
	w.Write([]byte("stored " + name))
}

func init() {
	http.HandleFunc("/uploads/finalize", finalize)
}
