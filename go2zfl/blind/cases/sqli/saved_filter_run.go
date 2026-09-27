package savedfilters

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

type FilterAPI struct {
	DB *sql.DB
}

// Save stores a named filter expression for the current user.
func (f *FilterAPI) Save(w http.ResponseWriter, r *http.Request) {
	name := r.PostFormValue("name")
	expr := r.PostFormValue("expression")
	owner := r.Header.Get("X-User-ID")
	if _, err := f.DB.Exec("INSERT INTO saved_filters (owner, name, expression) VALUES ($1, $2, $3)", owner, name, expr); err != nil {
		http.Error(w, "save failed", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusCreated)
}

// Run loads a stored filter and applies it to the orders table.
func (f *FilterAPI) Run(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(mux.Vars(r)["id"], 10, 64)
	if err != nil {
		http.Error(w, "bad id", http.StatusBadRequest)
		return
	}

	var expression string
	if err := f.DB.QueryRow("SELECT expression FROM saved_filters WHERE id = $1", id).Scan(&expression); err != nil {
		http.NotFound(w, r)
		return
	}

	rows, err := f.DB.Query("SELECT id, customer, total FROM orders WHERE " + expression)
	if err != nil {
		http.Error(w, "filter failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var ids []int64
	for rows.Next() {
		var oid int64
		var customer string
		var total float64
		if rows.Scan(&oid, &customer, &total) == nil {
			ids = append(ids, oid)
		}
	}
	json.NewEncoder(w).Encode(ids)
}

func (f *FilterAPI) Routes(r *mux.Router) {
	r.HandleFunc("/filters", f.Save).Methods("POST")
	r.HandleFunc("/filters/{id}/run", f.Run).Methods("GET")
}
