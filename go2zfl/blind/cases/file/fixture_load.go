package demo

import (
	"encoding/json"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gorilla/mux"
)

const fixturesDir = "./fixtures"

func loadFixture(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("set")
	if !filepath.IsLocal(name) {
		http.Error(w, "invalid fixture set", http.StatusBadRequest)
		return
	}
	raw, err := os.ReadFile(filepath.Join(fixturesDir, name+".json"))
	if err != nil {
		http.Error(w, "fixture set not found", http.StatusNotFound)
		return
	}
	var payload any
	if err := json.Unmarshal(raw, &payload); err != nil {
		http.Error(w, "corrupt fixture", http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(payload)
}

func Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/demo/fixtures", loadFixture).Methods("GET")
	return r
}
