package cartstate

import (
	"bytes"
	"encoding/json"
	"net/http"
)

type cartState struct {
	Coupon string   `json:"coupon"`
	Items  []string `json:"items"`
}

func CartPage(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	state := cartState{
		Coupon: r.Form.Get("coupon"),
		Items:  r.Form["item"],
	}

	var buf bytes.Buffer
	enc := json.NewEncoder(&buf)
	enc.SetEscapeHTML(false)
	if err := enc.Encode(state); err != nil {
		http.Error(w, "encode failed", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write([]byte("<html><body><div id=\"cart\"></div><script>window.__CART__ = "))
	w.Write(buf.Bytes())
	w.Write([]byte(";</script></body></html>"))
}
