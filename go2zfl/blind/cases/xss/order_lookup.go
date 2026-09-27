package orderlookup

import (
	"fmt"
	"net/http"

	"github.com/google/uuid"
)

func OrderBanner(w http.ResponseWriter, r *http.Request) {
	raw := r.URL.Query().Get("order")
	id, err := uuid.Parse(raw)
	if err != nil {
		http.Error(w, "invalid order id", http.StatusBadRequest)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<p>Tracking order <a href=\"/orders/%s\">%s</a></p>", id.String(), id)
}
