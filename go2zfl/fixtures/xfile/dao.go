package app
import "database/sql"
func Q(db *sql.DB, id string) { db.Query("SELECT * FROM u WHERE id=" + id) }  // id -> sql
