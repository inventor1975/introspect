package assets

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func serveAsset(w http.ResponseWriter, r *http.Request) {
	p := filepath.Clean(r.URL.Query().Get("src"))
	if strings.HasPrefix(p, "..") {
		http.Error(w, "forbidden", http.StatusForbidden)
		return
	}
	f, err := os.Open(p)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	defer f.Close()
	http.ServeContent(w, r, filepath.Base(p), time.Time{}, f)
}

func main() {
	os.Chdir("/srv/app/public")
	http.HandleFunc("/asset", serveAsset)
	http.ListenAndServe(":9000", nil)
}
