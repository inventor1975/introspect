package shop

import (
	"net/http"
	"os"
	"regexp"
)

var pattern = regexp.MustCompile(`^[a-z]+$`)

func One(w http.ResponseWriter, r *http.Request) {
	n := r.FormValue("n")
	if !pattern.MatchString(n) {
		return
	}
	os.Open("/srv/one/" + n)
}
