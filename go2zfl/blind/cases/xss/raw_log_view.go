package rawlogview

import (
	"fmt"
	"net/http"
	"time"
)

func LogLine(w http.ResponseWriter, r *http.Request) {
	msg := r.FormValue("msg")
	src := r.FormValue("source")

	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.Header().Set("X-Content-Type-Options", "nosniff")
	fmt.Fprintf(w, "%s [%s] <%s>\n", time.Now().UTC().Format(time.RFC3339), src, msg)
}
