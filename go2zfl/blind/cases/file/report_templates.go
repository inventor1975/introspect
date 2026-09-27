package reporting

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"sync"
)

type templateCatalog struct {
	mu    sync.RWMutex
	paths map[string]string
}

var catalog = &templateCatalog{paths: map[string]string{}}

func loadCatalog(configPath string) error {
	raw, err := os.ReadFile(configPath)
	if err != nil {
		return err
	}
	var cfg struct {
		Templates map[string]string `json:"templates"`
	}
	if err := json.Unmarshal(raw, &cfg); err != nil {
		return err
	}
	catalog.mu.Lock()
	catalog.paths = cfg.Templates
	catalog.mu.Unlock()
	return nil
}

func (c *templateCatalog) lookup(key string) (string, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	p, ok := c.paths[key]
	return p, ok
}

func reportTemplate(w http.ResponseWriter, r *http.Request) {
	path, ok := catalog.lookup(r.URL.Query().Get("template"))
	if !ok {
		http.Error(w, "unknown template", http.StatusNotFound)
		return
	}
	body, err := os.ReadFile(path)
	if err != nil {
		http.Error(w, "template unreadable", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.Write(body)
}

func main() {
	if err := loadCatalog(os.Getenv("REPORT_CATALOG")); err != nil {
		log.Fatalf("catalog: %v", err)
	}
	http.HandleFunc("/reports/template", reportTemplate)
	log.Fatal(http.ListenAndServe(":8084", nil))
}
