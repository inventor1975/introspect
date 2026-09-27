package invoicenote

import (
	"net/http"
	"text/template"
)

var noteTmpl = template.Must(template.New("note").Parse(`<!DOCTYPE html>
<html><body>
<h2>Invoice {{.Number}}</h2>
<p class="note">{{.Note}}</p>
</body></html>`))

type noteView struct {
	Number string
	Note   string
}

func InvoiceNoteHandler(w http.ResponseWriter, r *http.Request) {
	view := noteView{
		Number: r.URL.Query().Get("number"),
		Note:   r.URL.Query().Get("note"),
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := noteTmpl.Execute(w, view); err != nil {
		http.Error(w, "render failed", http.StatusInternalServerError)
	}
}
