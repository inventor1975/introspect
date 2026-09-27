package warehouse

import (
	"database/sql"
	"encoding/json"
	"net/http"

	"github.com/lib/pq"
)

type WarehouseAPI struct {
	DB *sql.DB
}

func (a *WarehouseAPI) Stock(w http.ResponseWriter, r *http.Request) {
	site := r.Header.Get("X-Site-Schema")
	if site == "" {
		site = "main"
	}

	query := "SELECT sku, qty FROM " + pq.QuoteIdentifier(site) + ".stock WHERE qty > $1"
	rows, err := a.DB.Query(query, 0)
	if err != nil {
		http.Error(w, "stock unavailable", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	stock := map[string]int{}
	for rows.Next() {
		var sku string
		var qty int
		if rows.Scan(&sku, &qty) == nil {
			stock[sku] = qty
		}
	}
	json.NewEncoder(w).Encode(stock)
}
