package forumsignature

import (
	"fmt"
	"html"
	"net/http"
)

// normalize turns entity-encoded input from the legacy editor back into text.
func normalize(s string) string {
	return html.UnescapeString(s)
}

func SignaturePreview(w http.ResponseWriter, r *http.Request) {
	sig := normalize(r.PostFormValue("signature"))
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<div class=\"signature\">%s</div>", sig)
}
