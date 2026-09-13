package main
import ("net/http"; "database/sql")
const CreateT = `CREATE TABLE IF NOT EXISTS u (id INT)`   // package-level constant DDL
func ddl(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	db.Exec(CreateT)                    // EXPECT: nothing (constant ident -> clean, not OPEN)
	id := r.FormValue("id")
	db.Exec("DELETE FROM u WHERE id=" + id)  // EXPECT: REFUTED [sql] (tainted concat)
}
