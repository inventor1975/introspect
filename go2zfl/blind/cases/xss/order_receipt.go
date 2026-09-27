package orderreceipt

import (
	"net/http"
	"text/template"
)

var receipt = template.Must(template.New("receipt").Parse(`<!DOCTYPE html>
<html><body>
<h2>Receipt</h2>
<p>Shipping to: {{.Name | html}}</p>
<p>Gift message: {{html .Gift}}</p>
</body></html>`))

func ReceiptHandler(w http.ResponseWriter, r *http.Request) {
	data := map[string]string{
		"Name": r.FormValue("name"),
		"Gift": r.FormValue("gift"),
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	receipt.Execute(w, data)
}
