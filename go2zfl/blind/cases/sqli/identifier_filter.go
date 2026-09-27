package exports

import (
	"database/sql"
	"encoding/csv"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

func identOnly(s string) string {
	return strings.Map(func(r rune) rune {
		switch {
		case r >= 'a' && r <= 'z', r >= '0' && r <= '9', r == '_':
			return r
		case r >= 'A' && r <= 'Z':
			return r + ('a' - 'A')
		}
		return -1
	}, s)
}

type ExportAPI struct {
	DB *sql.DB
}

func (e *ExportAPI) Column(w http.ResponseWriter, r *http.Request) {
	col := identOnly(mux.Vars(r)["column"])
	if col == "" {
		http.Error(w, "column required", http.StatusBadRequest)
		return
	}

	rows, err := e.DB.Query("SELECT id, " + col + " FROM customer_export ORDER BY id")
	if err != nil {
		http.Error(w, "export failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	w.Header().Set("Content-Type", "text/csv")
	cw := csv.NewWriter(w)
	for rows.Next() {
		var id, val string
		if rows.Scan(&id, &val) == nil {
			cw.Write([]string{id, val})
		}
	}
	cw.Flush()
}
