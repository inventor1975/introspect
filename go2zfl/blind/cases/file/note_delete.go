package notes

import (
	"encoding/json"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gorilla/mux"
)

type Server struct {
	NotesDir string
}

func (s *Server) Routes() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/notes", s.deleteNote).Methods(http.MethodDelete)
	return r
}

func (s *Server) deleteNote(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	target := filepath.Join(s.NotesDir, id)
	if err := os.Remove(target); err != nil {
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(map[string]string{"error": "note not found"})
		return
	}
	json.NewEncoder(w).Encode(map[string]string{"deleted": id})
}
