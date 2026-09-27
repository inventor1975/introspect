package colorswatch

import (
	"fmt"
	"html"
	"net/http"
)

func SwatchHandler(w http.ResponseWriter, r *http.Request) {
	color := html.EscapeString(r.URL.Query().Get("color"))
	label := html.EscapeString(r.URL.Query().Get("label"))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<div class=swatch data-color=%s>%s</div>", color, label)
}
