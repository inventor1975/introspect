package memberprofile

import (
	"io"
	"net/http"

	"github.com/gorilla/mux"
)

func ProfileHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	username := vars["username"]

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, "<html><body>")
	io.WriteString(w, "<div class=\"user\">Profile of "+username+"</div>")
	io.WriteString(w, "</body></html>")
}

func NewRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/members/{username}", ProfileHandler).Methods("GET")
	return r
}
