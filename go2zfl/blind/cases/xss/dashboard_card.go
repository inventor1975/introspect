package dashboardcard

import (
	"io"
	"net/http"

	"blindcases/xss/lib/pagekit"
)

func WidgetCard(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	title := q.Get("title")
	body := pagekit.Truncate(q.Get("body"), 500)

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, pagekit.Card(title, body))
}
