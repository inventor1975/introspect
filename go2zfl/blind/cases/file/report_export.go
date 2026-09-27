package reports

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

var exportDir = "/srv/reports/exports"

func exportPath(name string) string {
	return fmt.Sprintf("%s/%s.csv", exportDir, name)
}

func handleExport(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "bad form", http.StatusBadRequest)
		return
	}
	name := r.FormValue("name")
	data, err := os.ReadFile(exportPath(name))
	if err != nil {
		log.Printf("export %q: %v", name, err)
		http.Error(w, "export not available", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/csv")
	w.Header().Set("Content-Disposition", "attachment; filename=export.csv")
	w.Write(data)
}

func Register(mux *http.ServeMux) {
	mux.HandleFunc("/reports/export", handleExport)
}
