package ticketdetail

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

func TicketDetail(w http.ResponseWriter, r *http.Request) {
	idStr := mux.Vars(r)["id"]
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprint(w, "<p>Ticket ids are numeric.</p>")
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<h1>Ticket #%d</h1><a href=\"/tickets/%d/edit\">Edit</a>", id, id)
}

func Routes() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/tickets/{id}", TicketDetail).Methods(http.MethodGet)
	return r
}
