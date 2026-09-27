package directory

import (
	"database/sql"
	"encoding/json"
	"net/http"
)

type Employee struct {
	Name  string `json:"name"`
	Dept  string `json:"dept"`
	Phone string `json:"phone"`
}

type Directory struct {
	DB *sql.DB
}

func (d *Directory) ByDepartment(w http.ResponseWriter, r *http.Request) {
	dept := r.PostFormValue("department")

	stmt, err := d.DB.Prepare("SELECT name, dept, phone FROM employees WHERE dept = '" + dept + "' AND active = ?")
	if err != nil {
		http.Error(w, "prepare failed", http.StatusInternalServerError)
		return
	}
	defer stmt.Close()

	rows, err := stmt.Query(true)
	if err != nil {
		http.Error(w, "query failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var staff []Employee
	for rows.Next() {
		var e Employee
		if rows.Scan(&e.Name, &e.Dept, &e.Phone) == nil {
			staff = append(staff, e)
		}
	}
	json.NewEncoder(w).Encode(staff)
}
