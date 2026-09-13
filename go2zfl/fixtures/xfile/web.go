package app
import "net/http"
func Handle(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	id := r.FormValue("id")
	Q(db, id)                                    // EXPECT: REFUTED cross-file (Q param1 -> sql)
}
