package tagfilter

import (
	"bytes"
	"net/http"
	"sort"
)

func TagFilter(w http.ResponseWriter, r *http.Request) {
	tags := r.URL.Query()["tag"]
	sort.Strings(tags)

	seen := map[string]bool{}
	var buf bytes.Buffer
	buf.WriteString("<ul class=\"active-filters\">")
	for _, t := range tags {
		if seen[t] {
			continue
		}
		seen[t] = true
		buf.WriteString("<li><span class=\"tag\">")
		buf.WriteString(t)
		buf.WriteString("</span></li>")
	}
	buf.WriteString("</ul>")

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	buf.WriteTo(w)
}
