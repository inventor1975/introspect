package shipbatch

import (
	"database/sql"
	"encoding/json"
	"net/http"

	"example.com/billing/lib"
)

type Parcel struct {
	Code  string `json:"code"`
	Stage string `json:"stage"`
}

type BatchAPI struct {
	DB *sql.DB
}

func (b *BatchAPI) Lookup(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "bad form", http.StatusBadRequest)
		return
	}
	codes := r.Form["code"]
	if len(codes) == 0 || len(codes) > 100 {
		http.Error(w, "between 1 and 100 codes", http.StatusBadRequest)
		return
	}

	args := make([]interface{}, len(codes))
	for i, c := range codes {
		args[i] = c
	}
	query := "SELECT code, stage FROM parcels WHERE code IN (" + lib.Dollar(len(codes), 0) + ")"

	rows, err := b.DB.Query(query, args...)
	if err != nil {
		http.Error(w, "lookup failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var out []Parcel
	for rows.Next() {
		var p Parcel
		if rows.Scan(&p.Code, &p.Stage) == nil {
			out = append(out, p)
		}
	}
	json.NewEncoder(w).Encode(out)
}
