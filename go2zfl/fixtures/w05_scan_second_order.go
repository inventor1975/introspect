package fx

import (
	"database/sql"
	"fmt"
	"net/http"
)

// a value read back from the database: unknown (second order), not clean
func Show(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	var bio string
	db.QueryRow("SELECT bio FROM users WHERE id = 1").Scan(&bio)
	fmt.Fprintf(w, "<div>%s</div>", bio)
}
