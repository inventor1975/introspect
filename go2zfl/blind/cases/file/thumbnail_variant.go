package thumbs

import (
	"net/http"
	"os"
	"path/filepath"
	"regexp"
)

var numericID = regexp.MustCompile(`^[0-9]{1,18}$`)

var variantExt = map[string]string{
	"webp": ".webp",
	"avif": ".avif",
	"jpeg": ".jpg",
}

var contentTypes = map[string]string{
	".webp": "image/webp",
	".avif": "image/avif",
	".jpg":  "image/jpeg",
}

const variantDir = "/var/cache/thumb-variants"

func variant(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	id := q.Get("id")
	if !numericID.MatchString(id) {
		http.Error(w, "bad id", http.StatusBadRequest)
		return
	}
	ext, ok := variantExt[q.Get("format")]
	if !ok {
		ext = ".webp"
	}
	b, err := os.ReadFile(filepath.Join(variantDir, id+ext))
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", contentTypes[ext])
	w.Write(b)
}

func init() {
	http.HandleFunc("/thumb/variant", variant)
}
