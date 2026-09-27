package quantityupdate

import (
	"fmt"
	"net/http"
	"strconv"
)

func UpdateQuantity(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")

	qty, err := strconv.Atoi(r.FormValue("qty"))
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintf(w, "<div class=\"error\">Could not update cart: %v</div>", err)
		return
	}
	if qty < 1 || qty > 99 {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprint(w, "<div class=\"error\">Quantity out of range</div>")
		return
	}
	fmt.Fprintf(w, "<div class=\"ok\">Quantity set to %d</div>", qty)
}
