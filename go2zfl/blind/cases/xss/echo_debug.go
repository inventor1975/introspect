package echodebug

import (
	"io"
	"net/http"
)

// EchoBody returns the request payload so integrators can check what they sent.
func EchoBody(w http.ResponseWriter, r *http.Request) {
	payload := r.FormValue("payload")
	if payload == "" {
		io.WriteString(w, "empty payload")
		return
	}
	w.Write([]byte(payload))
}

func Mount(mux *http.ServeMux) {
	mux.HandleFunc("/debug/echo", EchoBody)
}
