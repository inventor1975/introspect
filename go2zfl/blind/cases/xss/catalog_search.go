package catalogsearch

import (
	"net/http"
	"strings"
)

type product struct {
	SKU   string
	Title string
}

var inventory = []product{
	{"A-100", "Walnut desk"},
	{"A-200", "Oak shelf"},
	{"B-310", "Desk lamp"},
}

func SearchHandler(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("q")

	var sb strings.Builder
	sb.WriteString("<!DOCTYPE html><html><body>")
	sb.WriteString("<p>Results for <em>" + q + "</em></p><ul>")
	found := 0
	for _, p := range inventory {
		if strings.Contains(strings.ToLower(p.Title), strings.ToLower(q)) {
			sb.WriteString("<li>" + p.SKU + " - " + p.Title + "</li>")
			found++
		}
	}
	if found == 0 {
		sb.WriteString("<li>No products matched.</li>")
	}
	sb.WriteString("</ul></body></html>")

	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(sb.String()))
}
