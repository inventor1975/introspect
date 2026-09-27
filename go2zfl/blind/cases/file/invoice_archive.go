package billing

import (
	"io"
	"net/http"
	"os"
	"path/filepath"
)

const archiveDir = "/var/lib/billing/archive"

func ArchivedInvoice(w http.ResponseWriter, r *http.Request) {
	name := filepath.Base(r.URL.Query().Get("file"))
	if name == "." || name == ".." || name == string(filepath.Separator) {
		http.Error(w, "invalid file", http.StatusBadRequest)
		return
	}
	f, err := os.Open(filepath.Join(archiveDir, name))
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	defer f.Close()
	w.Header().Set("Content-Type", "application/pdf")
	io.Copy(w, f)
}

func init() {
	http.HandleFunc("/invoices/archive", ArchivedInvoice)
}
