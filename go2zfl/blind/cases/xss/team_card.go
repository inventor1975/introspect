package teamcard

import (
	"io"
	"net/http"

	"blindcases/xss/lib/pagekit"
)

func TeamCard(w http.ResponseWriter, r *http.Request) {
	team := r.URL.Query().Get("team")
	motto := r.URL.Query().Get("motto")

	card := pagekit.Card(pagekit.Escape(team), pagekit.Escape(pagekit.Truncate(motto, 140)))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, pagekit.Layout(team, card))
}
