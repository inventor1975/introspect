package emailpreview

import (
	"html/template"
	"net/http"
)

type recipient struct {
	FirstName string
	Plan      string
}

func PreviewEmail(w http.ResponseWriter, r *http.Request) {
	header := r.FormValue("header")
	src := `<div class="mail-header">` + header + `</div>
<p>Hello {{.FirstName}}, your plan is {{.Plan}}.</p>`

	t, err := template.New("mail").Parse(src)
	if err != nil {
		http.Error(w, "template error", http.StatusBadRequest)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	t.Execute(w, recipient{FirstName: "Dana", Plan: "Pro"})
}
