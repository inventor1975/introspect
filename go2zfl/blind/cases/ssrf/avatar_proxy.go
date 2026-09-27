package avatarproxy

import (
	"io"
	"net/http"
)

func AvatarProxy(w http.ResponseWriter, r *http.Request) {
	src := r.URL.Query().Get("src")
	if src == "" {
		http.Error(w, "missing src", http.StatusBadRequest)
		return
	}
	resp, err := http.Get(src)
	if err != nil {
		http.Error(w, "upstream error", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
	w.Header().Set("Cache-Control", "public, max-age=86400")
	io.Copy(w, resp.Body)
}

func Register(mux *http.ServeMux) {
	mux.HandleFunc("/avatar", AvatarProxy)
}
