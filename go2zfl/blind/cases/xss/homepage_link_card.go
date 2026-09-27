package homepagelink

import (
	"html"
	"net/http"
	"strings"
)

func LinkCard(w http.ResponseWriter, r *http.Request) {
	homepage := strings.TrimSpace(r.FormValue("homepage"))
	display := r.FormValue("display")

	out := `<div class="link-card"><a href="` + html.EscapeString(homepage) + `">` +
		html.EscapeString(display) + `</a></div>`

	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(out))
}
