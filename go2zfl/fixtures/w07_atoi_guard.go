package fx

import (
	"database/sql"
	"fmt"
	"net/http"
	"os"
	"strconv"
)

func Order(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	id := r.FormValue("id")
	if _, err := strconv.Atoi(id); err != nil {
		return
	}
	db.Query("SELECT * FROM orders WHERE id = " + id) // numeric: validated by the parse
	os.Open("/srv/orders/" + id + ".json")
	qty := r.FormValue("qty")
	if _, err := strconv.Atoi(qty); err != nil {
		fmt.Fprintf(w, "<p>bad quantity: %v</p>", err) // the error quotes the input
	}
}
