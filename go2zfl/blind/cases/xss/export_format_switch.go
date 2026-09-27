package exportformat

import (
	"fmt"
	"html"
	"net/http"
)

func PreviewTitle(w http.ResponseWriter, r *http.Request) {
	title := r.FormValue("title")
	mode := r.FormValue("mode")

	var rendered string
	if mode == "rich" {
		rendered = title
	} else {
		rendered = html.EscapeString(title)
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<div class=\"preview\"><h1>%s</h1></div>", rendered)
}
