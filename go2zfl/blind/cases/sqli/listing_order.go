package listings

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

type Listing struct {
	ID    int     `json:"id"`
	Title string  `json:"title"`
	Price float64 `json:"price"`
}

type ListingsHandler struct {
	DB *sql.DB
}

func (h *ListingsHandler) Index(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()

	orderBy := "created_at"
	if s := q.Get("order_by"); s != "" {
		orderBy = s
	}
	dir := "DESC"
	if q.Get("asc") == "1" {
		dir = "ASC"
	}

	rows, err := h.DB.Query("SELECT id, title, price FROM listings WHERE visible = true ORDER BY " + orderBy + " " + dir)
	if err != nil {
		http.Error(w, "error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var res []Listing
	for rows.Next() {
		var l Listing
		if err := rows.Scan(&l.ID, &l.Title, &l.Price); err == nil {
			res = append(res, l)
		}
	}
	json.NewEncoder(w).Encode(res)
}
