package reportasync

import (
	"fmt"
	"net/http"
	"strings"
)

type section struct {
	order int
	html  string
}

func renderSection(order int, heading string, out chan<- section) {
	out <- section{order: order, html: "<h3>" + heading + "</h3>"}
}

func ReportHandler(w http.ResponseWriter, r *http.Request) {
	headings := strings.Split(r.URL.Query().Get("sections"), ",")
	results := make(chan section, len(headings))
	for i, h := range headings {
		go renderSection(i, h, results)
	}

	parts := make([]string, len(headings))
	for range headings {
		s := <-results
		parts[s.order] = s.html
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, "<div class=\"report\">"+strings.Join(parts, "\n")+"</div>")
}
