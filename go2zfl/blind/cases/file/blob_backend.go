package blobs

import (
	"context"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

type Backend interface {
	Get(ctx context.Context, key string) (io.ReadCloser, error)
}

type diskBackend struct {
	root string
}

func (d diskBackend) Get(ctx context.Context, key string) (io.ReadCloser, error) {
	return os.Open(filepath.Join(d.root, key))
}

var backends = map[string]func() Backend{
	"disk": func() Backend { return diskBackend{root: os.Getenv("BLOB_ROOT")} },
}

func Register(name string, factory func() Backend) {
	backends[name] = factory
}

type BlobHandler struct {
	backend Backend
}

func NewBlobHandler() *BlobHandler {
	kind := os.Getenv("BLOB_BACKEND")
	factory, ok := backends[kind]
	if !ok {
		factory = backends["disk"]
	}
	return &BlobHandler{backend: factory()}
}

func (h *BlobHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("key")
	rc, err := h.backend.Get(r.Context(), key)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	defer rc.Close()
	io.Copy(w, rc)
}
