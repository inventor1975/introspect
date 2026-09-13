package main
import ("net/http"; "database/sql")
func h3(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	id := r.FormValue("id")                     // source
	db.Query("SELECT * FROM u WHERE id=" + id)  // EXPECT: REFUTED [sql]
}
