package fx

import (
	"net/http"
	"net/url"
	"strings"
)

var partners = map[string]bool{"feeds.partner.example": true}

func Feed(w http.ResponseWriter, r *http.Request) {
	u, err := url.Parse(r.FormValue("feed"))
	if err != nil || u.Scheme != "https" {
		return
	}
	if !partners[strings.ToLower(u.Hostname())] {
		return
	}
	http.Get(u.String()) // the host is checked
	http.Get(r.FormValue("other"))
}
