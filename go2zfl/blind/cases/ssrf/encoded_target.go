package encodedtarget

import (
	"encoding/base64"
	"io"
	"net/http"
)

func Redirector(w http.ResponseWriter, r *http.Request) {
	token := r.URL.Query().Get("t")
	decoded, err := base64.RawURLEncoding.DecodeString(token)
	if err != nil {
		http.Error(w, "invalid token", http.StatusBadRequest)
		return
	}
	resp, err := http.Get(string(decoded))
	if err != nil {
		http.Error(w, "gone", http.StatusGone)
		return
	}
	defer resp.Body.Close()
	for k, v := range resp.Header {
		w.Header()[k] = v
	}
	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)
}
