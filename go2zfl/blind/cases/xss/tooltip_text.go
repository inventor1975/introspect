package tooltiptext

import (
	"fmt"
	"net/http"
	"strings"
)

var attrEscaper = strings.NewReplacer(
	"&", "&amp;",
	"<", "&lt;",
	">", "&gt;",
	`"`, "&#34;",
	"'", "&#39;",
)

func Tooltip(w http.ResponseWriter, r *http.Request) {
	hint := attrEscaper.Replace(r.URL.Query().Get("hint"))
	label := attrEscaper.Replace(r.URL.Query().Get("label"))
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<button type="button" title="%s" data-hint='%s'>%s</button>`, hint, hint, label)
}
