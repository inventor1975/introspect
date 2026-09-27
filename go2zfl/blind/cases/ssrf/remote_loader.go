package remoteloader

import (
	"io"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type Loader struct {
	client  *http.Client
	maxSize int64
}

func NewLoader() *Loader {
	return &Loader{client: &http.Client{Timeout: 10 * time.Second}, maxSize: 2 << 20}
}

func (l *Loader) load(location string) ([]byte, error) {
	resp, err := l.client.Get(location)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(io.LimitReader(resp.Body, l.maxSize))
}

type ConfigHandler struct {
	loader *Loader
}

func (h *ConfigHandler) Preview(w http.ResponseWriter, r *http.Request) {
	location := r.URL.Query().Get("location")
	data, err := h.loader.load(location)
	if err != nil {
		http.Error(w, "unable to load config", http.StatusBadGateway)
		return
	}
	w.Header().Set("Content-Type", "text/yaml")
	w.Write(data)
}

func Routes(r *mux.Router) {
	h := &ConfigHandler{loader: NewLoader()}
	r.HandleFunc("/config/preview", h.Preview).Methods("GET")
}
