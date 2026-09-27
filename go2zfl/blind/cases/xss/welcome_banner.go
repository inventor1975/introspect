package welcomebanner

import (
	"fmt"
	"net/http"
	"strings"
)

func WelcomeHandler(w http.ResponseWriter, r *http.Request) {
	name := strings.TrimSpace(r.FormValue("name"))
	if name == "" {
		name = "guest"
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<html><body><h1>Welcome back, %s!</h1></body></html>", name)
}

func Register(mux *http.ServeMux) {
	mux.HandleFunc("/welcome", WelcomeHandler)
}
