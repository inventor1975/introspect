package sharelinkbox

import (
	"fmt"
	"net/http"
	"net/url"
)

func ShareBox(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("q")
	shareURL := "/search?q=" + url.QueryEscape(q)

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<div class="share">
<a href="%s">Permalink</a>
<input readonly value="https://shop.example.com%s">
</div>`, shareURL, shareURL)
}
