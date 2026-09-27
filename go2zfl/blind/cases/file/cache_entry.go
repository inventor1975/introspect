package preview

import (
	"crypto/sha256"
	"encoding/hex"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

const cacheDir = "/var/cache/link-preview"

func cacheKey(u string) string {
	sum := sha256.Sum256([]byte(u))
	return hex.EncodeToString(sum[:])
}

func linkPreview(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("url")
	path := filepath.Join(cacheDir, cacheKey(target)+".html")
	if st, err := os.Stat(path); err == nil && time.Since(st.ModTime()) < time.Hour {
		data, err := os.ReadFile(path)
		if err == nil {
			w.Write(data)
			return
		}
	}
	body := []byte("<p>preview pending for " + cacheKey(target)[:12] + "</p>")
	os.WriteFile(path, body, 0o600)
	io.WriteString(w, string(body))
}

func init() {
	http.HandleFunc("/preview", linkPreview)
}
