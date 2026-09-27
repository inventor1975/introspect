package fulfilment

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

type Fulfilment struct {
	DB *sql.DB
}

func (f *Fulfilment) Lines(w http.ResponseWriter, r *http.Request) {
	orderID := mux.Vars(r)["orderID"]
	if _, err := strconv.Atoi(orderID); err != nil {
		http.Error(w, "order id must be numeric", http.StatusBadRequest)
		return
	}

	rows, err := f.DB.Query("SELECT sku, qty FROM order_lines WHERE order_id = " + orderID)
	if err != nil {
		http.Error(w, "lookup failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	lines := map[string]int{}
	for rows.Next() {
		var sku string
		var qty int
		if rows.Scan(&sku, &qty) == nil {
			lines[sku] = qty
		}
	}
	json.NewEncoder(w).Encode(lines)
}

func (f *Fulfilment) Routes(r *mux.Router) {
	r.HandleFunc("/orders/{orderID}/lines", f.Lines).Methods("GET")
}
