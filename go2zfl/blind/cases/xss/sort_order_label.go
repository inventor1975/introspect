package sortorderlabel

import (
	"fmt"
	"net/http"
)

func ListingHeader(w http.ResponseWriter, r *http.Request) {
	sort := r.URL.Query().Get("sort")

	var label string
	switch sort {
	case "price_asc":
		label = "Price: low to high"
	case "price_desc":
		label = "Price: high to low"
	case "newest":
		label = "Newest first"
	default:
		label = "Most relevant"
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<div class=\"sort\">Sorted by: <strong>%s</strong></div>", label)
}
