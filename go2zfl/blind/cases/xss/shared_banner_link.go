package sharedbanner

import (
	"encoding/base64"
	"net/http"
)

func BannerHandler(w http.ResponseWriter, r *http.Request) {
	encoded := r.URL.Query().Get("b")
	raw, err := base64.URLEncoding.DecodeString(encoded)
	if err != nil {
		http.Error(w, "invalid banner", http.StatusBadRequest)
		return
	}

	page := []byte("<html><body><div class=\"banner\">")
	page = append(page, raw...)
	page = append(page, []byte("</div></body></html>")...)

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write(page)
}
