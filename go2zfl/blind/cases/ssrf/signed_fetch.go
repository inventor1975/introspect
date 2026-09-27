package signedfetch

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"io"
	"net/http"
	"os"
)

var signingKey = []byte(os.Getenv("URL_SIGNING_KEY"))

func validSignature(target, sig string) bool {
	mac := hmac.New(sha256.New, signingKey)
	mac.Write([]byte(target))
	expected := mac.Sum(nil)
	given, err := hex.DecodeString(sig)
	if err != nil {
		return false
	}
	return hmac.Equal(expected, given)
}

func Media(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("u")
	if !validSignature(target, r.URL.Query().Get("sig")) {
		http.Error(w, "invalid signature", http.StatusForbidden)
		return
	}
	resp, err := http.Get(target)
	if err != nil {
		http.Error(w, "media unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
	io.Copy(w, resp.Body)
}
