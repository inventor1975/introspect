package upstreamconfig

import (
	"encoding/json"
	"io"
	"net/http"
	"os"
)

type Config struct {
	Upstreams map[string]string `json:"upstreams"`
}

func LoadConfig(path string) (*Config, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var cfg Config
	err = json.NewDecoder(f).Decode(&cfg)
	return &cfg, err
}

type Gateway struct {
	cfg *Config
}

func (g *Gateway) Call(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("upstream")
	base, ok := g.cfg.Upstreams[name]
	if !ok {
		http.Error(w, "unknown upstream", http.StatusNotFound)
		return
	}
	resp, err := http.Get(base + "/v1/info")
	if err != nil {
		http.Error(w, "upstream error", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, resp.Body)
}

func New() (*Gateway, error) {
	cfg, err := LoadConfig("/etc/gateway/upstreams.json")
	if err != nil {
		return nil, err
	}
	return &Gateway{cfg: cfg}, nil
}
