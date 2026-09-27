package subscriptionstate

import (
	"fmt"
	"net/http"
)

func StatusPill(w http.ResponseWriter, r *http.Request) {
	status := r.URL.Query().Get("status")
	if status == "active" {
		status = "Active"
	} else if status == "paused" {
		status = "Paused"
	} else {
		status = "Cancelled"
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<span class=\"pill\">%s</span>", status)
}
