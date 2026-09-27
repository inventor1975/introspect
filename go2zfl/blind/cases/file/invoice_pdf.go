package billing

import (
	"io"
	"net/http"
	"os"
	"path/filepath"
)

const invoiceDir = "/var/lib/billing/invoices"

// InvoicePDF streams a stored invoice back to the customer portal.
func InvoicePDF(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("file")
	if name == "" {
		http.Error(w, "missing file", http.StatusBadRequest)
		return
	}
	f, err := os.Open(filepath.Join(invoiceDir, name))
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	defer f.Close()
	w.Header().Set("Content-Type", "application/pdf")
	io.Copy(w, f)
}

func main() {
	http.HandleFunc("/invoices/pdf", InvoicePDF)
	http.ListenAndServe(":8080", nil)
}
