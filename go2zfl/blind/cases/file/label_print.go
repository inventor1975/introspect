package warehouse

import (
	"net/http"
	"os"
	"path/filepath"
	"regexp"
)

var labelName = regexp.MustCompile(`[a-zA-Z0-9_-]+`)

const labelDir = "/var/warehouse/labels"

func printLabel(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("label")
	if !labelName.MatchString(id) {
		http.Error(w, "bad label id", http.StatusBadRequest)
		return
	}
	zpl, err := os.ReadFile(filepath.Join(labelDir, id+".zpl"))
	if err != nil {
		http.Error(w, "label not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "application/x-zpl")
	w.Write(zpl)
}

func init() {
	http.HandleFunc("/labels/print", printLabel)
}
