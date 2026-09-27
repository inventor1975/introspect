package loopbackblock

import (
	"io"
	"net/http"
	"net/url"
	"strings"
)

var blocked = []string{"localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254"}

func isBlocked(raw string) bool {
	u, err := url.Parse(raw)
	if err != nil {
		return true
	}
	host := strings.ToLower(u.Hostname())
	for _, b := range blocked {
		if host == b {
			return true
		}
	}
	return false
}

func Import(w http.ResponseWriter, r *http.Request) {
	src := r.FormValue("src")
	if isBlocked(src) {
		http.Error(w, "forbidden destination", http.StatusForbidden)
		return
	}
	resp, err := http.Get(src)
	if err != nil {
		http.Error(w, "fetch failed", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, resp.Body)
}
