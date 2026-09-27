package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

func main() {
	db, err := sql.Open("postgres", "postgres://app@localhost/shop?sslmode=disable")
	if err != nil {
		log.Fatal(err)
	}

	r := mux.NewRouter()
	r.HandleFunc("/brands/{brand}/count", func(w http.ResponseWriter, req *http.Request) {
		brand := mux.Vars(req)["brand"]
		var n int
		if err := db.QueryRow("SELECT count(*) FROM products WHERE brand = '" + brand + "'").Scan(&n); err != nil {
			http.Error(w, "count failed", http.StatusInternalServerError)
			return
		}
		json.NewEncoder(w).Encode(map[string]int{"count": n})
	}).Methods("GET")

	log.Fatal(http.ListenAndServe(":8080", r))
}
