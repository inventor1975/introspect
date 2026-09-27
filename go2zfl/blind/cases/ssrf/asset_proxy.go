package assetproxy

import (
	"io"
	"net/http"

	"example.com/blindsvc/lib/allow"
)

func Asset(w http.ResponseWriter, r *http.Request) {
	u, err := allow.Check(r.URL.Query().Get("src"))
	if err != nil {
		http.Error(w, "asset host not allowed", http.StatusForbidden)
		return
	}
	resp, err := http.Get(u.String())
	if err != nil {
		http.Error(w, "asset unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
	io.Copy(w, resp.Body)
}
