package mirrorindex

import (
	"io"
	"net/http"
	"net/url"
	"strconv"

	"github.com/gorilla/mux"
)

var mirrors = []string{
	"https://mirror1.pkgs.acme.io",
	"https://mirror2.pkgs.acme.io",
	"https://eu.mirror.pkgs.acme.io",
}

func Download(w http.ResponseWriter, r *http.Request) {
	idx, err := strconv.Atoi(r.URL.Query().Get("mirror"))
	if err != nil || idx < 0 || idx >= len(mirrors) {
		idx = 0
	}
	pkg := mux.Vars(r)["pkg"]
	resp, err := http.Get(mirrors[idx] + "/index/" + url.PathEscape(pkg))
	if err != nil {
		http.Error(w, "mirror unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, resp.Body)
}
