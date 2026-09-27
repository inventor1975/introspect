package eventpage

import (
	"net/http"
	"strings"
)

type Event struct {
	Title    string
	Venue    string
	Capacity int
}

func (e Event) HTML() string {
	var b strings.Builder
	b.WriteString("<div class=\"event\">")
	b.WriteString("<h2>" + e.Title + "</h2>")
	b.WriteString("<span class=\"venue\">" + e.Venue + "</span>")
	b.WriteString("</div>")
	return b.String()
}

func eventFromRequest(r *http.Request) Event {
	return Event{
		Title:    r.PostFormValue("title"),
		Venue:    r.PostFormValue("venue"),
		Capacity: 100,
	}
}

func DraftPreview(w http.ResponseWriter, r *http.Request) {
	ev := eventFromRequest(r)
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write([]byte(ev.HTML()))
}
