package main
import ("net/http"; "database/sql"; "fmt")
func pq(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	id := r.FormValue("id")
	// UNSAFE: concatenated/Sprintf query straight to Query
	db.Query(fmt.Sprintf("SELECT * FROM u WHERE id=%s", id))   // EXPECT: REFUTED [sql]
	// SAFE: constant SQL with ? placeholder, prepared, value passed as BOUND param
	stmt, _ := db.Prepare("SELECT * FROM u WHERE id=?")
	stmt.QueryRow(id)                                          // EXPECT: nothing (bound param, not SQL)
}
