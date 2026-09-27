package checkoutstate

import (
	"encoding/json"
	"net/http"
)

type checkout struct {
	Coupon  string `json:"coupon"`
	Country string `json:"country"`
}

func CheckoutPage(w http.ResponseWriter, r *http.Request) {
	state := checkout{
		Coupon:  r.FormValue("coupon"),
		Country: r.FormValue("country"),
	}
	blob, err := json.Marshal(state)
	if err != nil {
		http.Error(w, "encode failed", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write([]byte("<html><body><div id=\"checkout\"></div><script>window.__CHECKOUT__ = "))
	w.Write(blob)
	w.Write([]byte(";</script></body></html>"))
}
