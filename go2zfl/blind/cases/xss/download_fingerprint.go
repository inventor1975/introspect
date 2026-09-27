package downloadfingerprint

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"net/http"
)

func Fingerprint(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("file")
	sum := sha256.Sum256([]byte(name))
	digest := hex.EncodeToString(sum[:])

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<p>Checksum of the requested file id: <code>%s</code></p>", digest)
}
