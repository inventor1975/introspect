package fx

import (
	"net/http"
	"net/url"
	"time"
)

type Fetcher struct {
	client *http.Client
}

func (f *Fetcher) Probe(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("target")
	f.client.Get(target) // a client kept in a struct field
	req, _ := http.NewRequest("GET", r.FormValue("hook"), nil)
	c := &http.Client{Timeout: time.Second}
	c.Do(req)
	// fixed scheme://host/ and an escaped query value: the host cannot move
	http.Get("https://api.example.com/search?q=" + url.QueryEscape(r.FormValue("q")))
}
