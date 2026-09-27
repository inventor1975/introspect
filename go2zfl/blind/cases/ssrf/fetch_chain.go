package fetchchain

import (
	"io"
	"net/http"
	"strings"
)

func buildTarget(r *http.Request) string {
	t := strings.TrimSpace(r.FormValue("target"))
	if !strings.Contains(t, "://") {
		t = "http://" + t
	}
	return t
}

func proxyTo(w http.ResponseWriter, target string) error {
	req, err := http.NewRequest("GET", target, nil)
	if err != nil {
		return err
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	w.WriteHeader(resp.StatusCode)
	_, err = io.Copy(w, resp.Body)
	return err
}

func Relay(w http.ResponseWriter, r *http.Request) {
	if err := proxyTo(w, buildTarget(r)); err != nil {
		http.Error(w, "relay failed", http.StatusBadGateway)
	}
}
