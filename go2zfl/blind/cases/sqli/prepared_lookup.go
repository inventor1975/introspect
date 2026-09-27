package staff

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
	byDept *sql.Stmt
}

func NewDirectory(db *sql.DB) (*Directory, error) {
	st, err := db.Prepare("SELECT name, dept, phone FROM employees WHERE dept = ? AND active = 1")
	if err != nil {
		return nil, err
	}
	return &Directory{byDept: st}, nil
}

func (d *Directory) ByDepartment(w http.ResponseWriter, r *http.Request) {
	dept := r.PostFormValue("department")

	rows, err := d.byDept.Query(dept)
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
