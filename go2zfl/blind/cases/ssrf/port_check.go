package portcheck

import (
	"encoding/json"
	"net"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

func CheckPort(w http.ResponseWriter, r *http.Request) {
	host := r.FormValue("host")
	port := r.FormValue("port")
	addr := net.JoinHostPort(host, port)
	conn, err := net.DialTimeout("tcp", addr, 2*time.Second)
	open := err == nil
	if open {
		conn.Close()
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"addr": addr, "open": open})
}

func Mount(r *mux.Router) {
	r.HandleFunc("/tools/port-check", CheckPort).Methods("POST")
}
