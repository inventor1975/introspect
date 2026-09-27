package trackingsnippet

import (
	"fmt"
	"net/http"
	"strconv"
)

func LandingPage(w http.ResponseWriter, r *http.Request) {
	campaign := r.URL.Query().Get("utm_campaign")

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, "<html><head><script>\n")
	fmt.Fprintf(w, "window.analyticsCampaign = %s;\n", strconv.Quote(campaign))
	fmt.Fprint(w, "</script></head><body><h1>Spring sale</h1></body></html>")
}
