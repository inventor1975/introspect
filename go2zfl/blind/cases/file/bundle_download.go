package bundles

import (
	"archive/zip"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

const sharedDir = "/srv/shared/files"

func downloadBundle(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	var names []string
	for _, v := range r.Form["f"] {
		for _, part := range strings.Split(v, ",") {
			if part = strings.TrimSpace(part); part != "" {
				names = append(names, part)
			}
		}
	}
	if len(names) == 0 {
		http.Error(w, "no files selected", http.StatusBadRequest)
		return
	}
	w.Header().Set("Content-Type", "application/zip")
	w.Header().Set("Content-Disposition", `attachment; filename="bundle.zip"`)
	zw := zip.NewWriter(w)
	defer zw.Close()
	for _, n := range names {
		data, err := os.ReadFile(filepath.Join(sharedDir, n))
		if err != nil {
			continue
		}
		entry, err := zw.Create(filepath.Base(n))
		if err != nil {
			return
		}
		entry.Write(data)
	}
}

func init() {
	http.HandleFunc("/bundle", downloadBundle)
}
