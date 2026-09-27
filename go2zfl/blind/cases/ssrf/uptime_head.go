package uptimehead

import (
	"fmt"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

func Ping(w http.ResponseWriter, r *http.Request) {
	probe := r.URL.Query().Get("probe")
	start := time.Now()
	resp, err := http.Head(probe)
	if err != nil {
		fmt.Fprintf(w, "down: %v\n", err)
		return
	}
	resp.Body.Close()
	fmt.Fprintf(w, "up: %d in %s\n", resp.StatusCode, time.Since(start))
}

func NewRouter() http.Handler {
	r := mux.NewRouter()
	r.HandleFunc("/uptime", Ping).Queries("probe", "{probe}")
	return r
}
