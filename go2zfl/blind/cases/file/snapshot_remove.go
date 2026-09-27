package snapshots

import (
	"errors"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gorilla/mux"
)

type Manager struct {
	Root string
}

func checkSnapshotName(name string) error {
	if name == "" {
		return errors.New("empty snapshot name")
	}
	if strings.ContainsAny(name, `/\`) || name == "." || name == ".." {
		return errors.New("snapshot name must be a single path element")
	}
	return nil
}

func (m *Manager) Delete(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("snapshot")
	if err := checkSnapshotName(name); err != nil {
		log.Printf("snapshot delete: suspicious name %q: %v", name, err)
	}
	if err := os.RemoveAll(filepath.Join(m.Root, name)); err != nil {
		http.Error(w, "delete failed", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (m *Manager) Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/snapshots/delete", m.Delete).Methods(http.MethodPost)
	return r
}
