package totals

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"time"
)

type TotalsHandler struct {
	DB *sql.DB
}

func (h *TotalsHandler) ForDay(w http.ResponseWriter, r *http.Request) {
	dayParam := r.URL.Query().Get("day")
	day, err := time.Parse("2006-01-02", dayParam)
	if err != nil {
		http.Error(w, "day must be YYYY-MM-DD", http.StatusBadRequest)
		return
	}

	stamp := day.Format("2006-01-02")
	var count int
	var sum float64
	err = h.DB.QueryRow("SELECT COUNT(*), COALESCE(SUM(amount),0) FROM payments WHERE paid_on = '" + stamp + "'").Scan(&count, &sum)
	if err != nil {
		http.Error(w, "totals failed", http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"day": stamp, "count": count, "sum": sum})
}
