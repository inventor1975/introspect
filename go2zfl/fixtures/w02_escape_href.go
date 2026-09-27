package fx

import (
	"html"
	"net/http"
)

// html.EscapeString protects text, not the START of an href (javascript: survives)
func Card(w http.ResponseWriter, r *http.Request) {
	site := r.FormValue("site")
	label := r.FormValue("label")
	out := `<a href="` + html.EscapeString(site) + `">` + html.EscapeString(label) + `</a>`
	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(out))
}
