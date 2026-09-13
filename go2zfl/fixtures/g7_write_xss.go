package main
import ("net/http"; "database/sql")
func wx(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	q := r.FormValue("q")
	w.Write([]byte(q))                  // EXPECT: REFUTED [xss] (receiver-typed ResponseWriter)
	db.Query("SELECT 1")                // constant: EXPECT nothing (no FP)
}
