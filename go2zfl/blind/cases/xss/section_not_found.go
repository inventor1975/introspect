package sectionnotfound

import (
	"fmt"
	"net/http"
	"strings"
)

var sections = map[string]string{
	"news":   "<h1>News</h1>",
	"events": "<h1>Events</h1>",
}

func SectionHandler(w http.ResponseWriter, r *http.Request) {
	name := strings.TrimPrefix(r.URL.Path, "/section/")
	body, ok := sections[name]
	if !ok {
		http.Error(w, fmt.Sprintf("unknown section <%s>", name), http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, body)
}
