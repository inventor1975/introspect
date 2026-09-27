package projectslug

import (
	"io"
	"net/http"
	"regexp"

	"github.com/gorilla/mux"
)

var slugRe = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{0,62}$`)

func ProjectHeader(w http.ResponseWriter, r *http.Request) {
	slug := mux.Vars(r)["slug"]
	if !slugRe.MatchString(slug) {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, "<header><h1>Project "+slug+"</h1><a href=\"/p/"+slug+"/settings\">Settings</a></header>")
}

func Mount(r *mux.Router) {
	r.HandleFunc("/p/{slug}", ProjectHeader)
}
