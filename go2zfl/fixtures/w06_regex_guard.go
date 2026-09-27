package fx

import (
	"net/http"
	"os"
	"path/filepath"
	"regexp"
)

var anchored = regexp.MustCompile(`^[a-z0-9]{4,32}$`)
var loose = regexp.MustCompile(`[a-z0-9]+`)

func Doc(w http.ResponseWriter, r *http.Request) {
	a := r.FormValue("a")
	if !anchored.MatchString(a) {
		return
	}
	os.ReadFile(filepath.Join("/srv/docs", a))
	b := r.FormValue("b")
	if !loose.MatchString(b) { // a substring match: ../x passes
		return
	}
	os.ReadFile(filepath.Join("/srv/docs", b))
}
