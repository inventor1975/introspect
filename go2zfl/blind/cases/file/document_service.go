package documents

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

type DocumentService struct {
	root      string
	maxLength int
}

func NewDocumentService(root string) *DocumentService {
	return &DocumentService{root: root, maxLength: 128}
}

func (s *DocumentService) locate(name string) string {
	name = strings.TrimSpace(name)
	return filepath.Join(s.root, name)
}

func (s *DocumentService) Read(name string) ([]byte, error) {
	if len(name) > s.maxLength {
		return nil, os.ErrInvalid
	}
	return os.ReadFile(s.locate(name))
}

type DocumentController struct {
	svc *DocumentService
}

func (dc *DocumentController) Get(w http.ResponseWriter, r *http.Request) {
	body, err := dc.svc.Read(r.URL.Query().Get("name"))
	if err != nil {
		http.Error(w, "document unavailable", http.StatusNotFound)
		return
	}
	w.Write(body)
}

func Register(mux *http.ServeMux) {
	dc := &DocumentController{svc: NewDocumentService("/srv/documents")}
	mux.HandleFunc("/documents", dc.Get)
}
