package messageformat

import (
	"html"
	"html/template"
	"io"
	"net/http"
)

func RenderMessage(w http.ResponseWriter, r *http.Request) {
	msg := r.FormValue("msg")
	var out string
	if r.FormValue("legacy") == "1" {
		out = template.HTMLEscapeString(msg)
	} else {
		out = html.EscapeString(msg)
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, "<blockquote>"+out+"</blockquote>")
}
