package shop

import (
	"net/http"
	"os"
	"regexp"
)

// the same package NAME in another directory: another package, another `pattern`
var pattern = regexp.MustCompile(`[a-z]+`)

func Two(w http.ResponseWriter, r *http.Request) {
	n := r.FormValue("n")
	if !pattern.MatchString(n) {
		return
	}
	os.Open("/srv/two/" + n)
}
