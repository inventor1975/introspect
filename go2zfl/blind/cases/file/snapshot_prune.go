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

type Pruner struct {
	Root string
}

func snapshotName(name string) error {
	if name == "" {
		return errors.New("empty snapshot name")
	}
	if strings.ContainsAny(name, `/\`) || name == "." || name == ".." {
		return errors.New("snapshot name must be a single path element")
	}
	return nil
}

func (p *Pruner) Prune(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("snapshot")
	if err := snapshotName(name); err != nil {
		log.Printf("snapshot prune rejected %q: %v", name, err)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if err := os.RemoveAll(filepath.Join(p.Root, name)); err != nil {
		http.Error(w, "prune failed", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (p *Pruner) Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/snapshots/prune", p.Prune).Methods(http.MethodPost)
	return r
}
