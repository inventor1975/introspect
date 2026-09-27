package invoices

import (
	"database/sql"
	"encoding/json"
	"net/http"

	"example.com/billing/lib"
)

type Invoice struct {
	Number string  `json:"number"`
	Amount float64 `json:"amount"`
	State  string  `json:"state"`
}

type InvoiceService struct {
	DB *sql.DB
}

func (s *InvoiceService) ListByCustomer(w http.ResponseWriter, r *http.Request) {
	customer := r.URL.Query().Get("customer")

	stmt := "SELECT number, amount, state FROM invoices WHERE " + lib.WhereEquals("customer_ref", customer)
	rows, err := s.DB.Query(stmt)
	if err != nil {
		http.Error(w, "db error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var list []Invoice
	for rows.Next() {
		var inv Invoice
		if rows.Scan(&inv.Number, &inv.Amount, &inv.State) == nil {
			list = append(list, inv)
		}
	}
	json.NewEncoder(w).Encode(list)
}
