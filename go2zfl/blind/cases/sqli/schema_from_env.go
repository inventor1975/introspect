package reporting

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type ReportingAPI struct {
	DB     *sql.DB
	schema string
}

func NewReportingAPI(db *sql.DB) *ReportingAPI {
	schema := os.Getenv("REPORTING_SCHEMA")
	if schema == "" {
		schema = "analytics"
	}
	return &ReportingAPI{DB: db, schema: schema}
}

func (a *ReportingAPI) Monthly(w http.ResponseWriter, r *http.Request) {
	month := r.URL.Query().Get("month")

	q := fmt.Sprintf("SELECT channel, revenue FROM %s.monthly_revenue WHERE month = $1", a.schema)
	rows, err := a.DB.Query(q, month)
	if err != nil {
		http.Error(w, "report failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	out := map[string]float64{}
	for rows.Next() {
		var ch string
		var rev float64
		if rows.Scan(&ch, &rev) == nil {
			out[ch] = rev
		}
	}
	json.NewEncoder(w).Encode(out)
}
