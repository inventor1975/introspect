package manuals

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

const manualsDir = "/usr/share/product/manuals"

func validManualName(name string) bool {
	return name != "" && !strings.Contains(name, "..") && !strings.HasPrefix(name, "/")
}

func manualHandler(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("topic")
	if !validManualName(name) {
		http.Error(w, "unknown topic", http.StatusBadRequest)
	}
	page, err := os.ReadFile(filepath.Join(manualsDir, name+".html"))
	if err != nil {
		http.Error(w, "missing manual page", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write(page)
}

func main() {
	http.HandleFunc("/manual", manualHandler)
	http.ListenAndServe(":8000", nil)
}
