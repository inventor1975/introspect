package htmlescapedurl

import (
	"fmt"
	"html"
	"io"
	"net/http"
)

func EmbedSnippet(w http.ResponseWriter, r *http.Request) {
	target := html.EscapeString(r.FormValue("url"))
	resp, err := http.Get(target)
	if err != nil {
		fmt.Fprintf(w, "<p>Could not load %s</p>", target)
		return
	}
	defer resp.Body.Close()
	snippet, _ := io.ReadAll(io.LimitReader(resp.Body, 4096))
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<blockquote cite=\"%s\"><pre>%s</pre></blockquote>", target, html.EscapeString(string(snippet)))
}
