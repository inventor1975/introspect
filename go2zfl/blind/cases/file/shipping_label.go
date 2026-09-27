package shipping

import (
	"net/http"
	"os"
	"path/filepath"
	"regexp"

	"github.com/gorilla/mux"
)

var trackingPattern = regexp.MustCompile(`^[A-Z0-9_-]{6,40}$`)

type LabelService struct {
	Dir string
}

func (s *LabelService) Label(w http.ResponseWriter, r *http.Request) {
	tracking := r.FormValue("tracking")
	if !trackingPattern.MatchString(tracking) {
		http.Error(w, "invalid tracking number", http.StatusBadRequest)
		return
	}
	pdf, err := os.ReadFile(filepath.Join(s.Dir, tracking+".pdf"))
	if err != nil {
		http.Error(w, "label not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "application/pdf")
	w.Write(pdf)
}

func (s *LabelService) Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/shipping/label", s.Label).Methods("GET")
	return r
}
