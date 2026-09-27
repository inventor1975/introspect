package catalog

import (
	"database/sql"
	"fmt"
	"html"
	"net/http"
)

type CatalogHandler struct {
	DB *sql.DB
}

func (h *CatalogHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	pid := html.EscapeString(r.URL.Query().Get("pid"))

	var name, descr string
	var price float64
	row := h.DB.QueryRow("SELECT name, description, price FROM products WHERE product_id = " + pid)
	if err := row.Scan(&name, &descr, &price); err != nil {
		http.Error(w, "product not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<h1>%s</h1><p>%s</p><p>%.2f</p>",
		html.EscapeString(name), html.EscapeString(descr), price)
}
