package reports

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
)

var annualDir = "/srv/reports/annual"

func annualReport(w http.ResponseWriter, r *http.Request) {
	year, err := strconv.Atoi(r.FormValue("year"))
	if err != nil || year < 2000 || year > 2100 {
		http.Error(w, "year out of range", http.StatusBadRequest)
		return
	}
	path := fmt.Sprintf("%s/%d.csv", annualDir, year)
	data, err := os.ReadFile(path)
	if err != nil {
		http.Error(w, "report not published yet", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/csv")
	w.Write(data)
}

func init() {
	http.HandleFunc("/reports/annual", annualReport)
}
