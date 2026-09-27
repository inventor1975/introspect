package orders

import (
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/gorilla/mux"
)

type InvoiceHandler struct {
	Dir string
}

func (h *InvoiceHandler) Get(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	orderID, err := strconv.ParseInt(vars["id"], 10, 64)
	if err != nil {
		http.Error(w, "invalid order id", http.StatusBadRequest)
		return
	}
	f, err := os.Open(fmt.Sprintf("%s/order-%d.pdf", h.Dir, orderID))
	if err != nil {
		http.Error(w, "invoice not ready", http.StatusNotFound)
		return
	}
	defer f.Close()
	st, _ := f.Stat()
	http.ServeContent(w, r, fmt.Sprintf("order-%d.pdf", orderID), st.ModTime(), f)
}

func NewRouter(h *InvoiceHandler) *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/orders/{id:[0-9]+}/invoice", h.Get).Methods("GET")
	return r
}
