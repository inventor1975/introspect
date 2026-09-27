package stats

import (
	"database/sql"
	"fmt"
	"net/http"
)

type StatsServer struct {
	db *sql.DB
}

func (s *StatsServer) regionTotals(w http.ResponseWriter, r *http.Request) {
	region := "eu-west"
	if ck, err := r.Cookie("preferred_region"); err == nil && ck.Value != "" {
		region = ck.Value
	}

	var orders int
	var revenue float64
	q := "SELECT COUNT(*), COALESCE(SUM(total), 0) FROM orders WHERE region = '" + region + "'"
	if err := s.db.QueryRow(q).Scan(&orders, &revenue); err != nil {
		http.Error(w, "stats unavailable", http.StatusInternalServerError)
		return
	}
	fmt.Fprintf(w, "region=%s orders=%d revenue=%.2f\n", region, orders, revenue)
}

func (s *StatsServer) Install(mux *http.ServeMux) {
	mux.HandleFunc("/stats/region", s.regionTotals)
}
