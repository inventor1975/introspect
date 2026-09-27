package fx

import (
	"net/http"
	"os"
)

func Export(w http.ResponseWriter, r *http.Request) {
	target := "/srv/export/latest.csv"
	if r.FormValue("preview") != "" {
		target := r.FormValue("preview") // a NEW variable in the if block
		w.Write([]byte("preview of " + target))
	}
	os.Open(target) // the outer, constant target
}
