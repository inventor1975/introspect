package greetingcard

import (
	"fmt"
	"html"
	"net/http"
)

func CardHandler(w http.ResponseWriter, r *http.Request) {
	to := r.FormValue("to")
	from := r.FormValue("from")
	msg := r.FormValue("message")

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<div class="card" title="%s">
<p>Dear %s,</p>
<p>%s</p>
<p>- %s</p>
</div>`, html.EscapeString(to), html.EscapeString(to), html.EscapeString(msg), html.EscapeString(from))
}
