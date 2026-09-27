package paginationlinks

import (
	"fmt"
	"net/http"
	"strconv"
)

func PageNav(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")

	pageStr := r.URL.Query().Get("page")
	page, err := strconv.Atoi(pageStr)
	if err != nil || page < 1 {
		page = 1
	}
	fmt.Fprintf(w, "<nav><a href=\"?page=%d\">Previous</a> <span>Page %d</span> <a href=\"?page=%d\">Next</a></nav>",
		page-1, page, page+1)
}
