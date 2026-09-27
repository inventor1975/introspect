package recentsearches

import (
	"fmt"
	"net/http"
	"sync"
)

var (
	mu     sync.Mutex
	recent []string
)

func Search(w http.ResponseWriter, r *http.Request) {
	term := r.URL.Query().Get("term")
	mu.Lock()
	recent = append(recent, term)
	if len(recent) > 10 {
		recent = recent[1:]
	}
	mu.Unlock()
	http.Redirect(w, r, "/results?term="+term, http.StatusFound)
}

func Trending(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	snapshot := append([]string(nil), recent...)
	mu.Unlock()

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, "<h2>People are searching for</h2><ol>")
	for _, t := range snapshot {
		fmt.Fprintf(w, "<li>%s</li>", t)
	}
	fmt.Fprint(w, "</ol>")
}
