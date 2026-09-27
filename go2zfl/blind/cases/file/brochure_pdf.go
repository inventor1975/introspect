package marketing

import (
	"net/http"
)

var brochures = http.Dir("/srv/marketing/brochures")

func brochure(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("f")
	f, err := brochures.Open(name)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	defer f.Close()
	st, err := f.Stat()
	if err != nil || st.IsDir() {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "application/pdf")
	http.ServeContent(w, r, st.Name(), st.ModTime(), f)
}

func init() {
	http.HandleFunc("/brochure", brochure)
}
