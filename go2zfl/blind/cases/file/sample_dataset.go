package datasets

import (
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"

	"github.com/gorilla/mux"
)

var samples = []string{
	"iris.csv",
	"titanic.csv",
	"housing.parquet",
	"airline-delays.csv",
}

const samplesDir = "/srv/datasets/samples"

func sample(w http.ResponseWriter, r *http.Request) {
	idx, err := strconv.Atoi(r.URL.Query().Get("n"))
	if err != nil || idx < 0 || idx >= len(samples) {
		http.Error(w, "unknown sample", http.StatusBadRequest)
		return
	}
	f, err := os.Open(filepath.Join(samplesDir, samples[idx]))
	if err != nil {
		http.Error(w, "sample missing", http.StatusInternalServerError)
		return
	}
	defer f.Close()
	w.Header().Set("Content-Disposition", "attachment; filename="+samples[idx])
	io.Copy(w, f)
}

func Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/datasets/sample", sample)
	return r
}
