package reviewsanitized

import (
	"html/template"
	"net/http"

	"github.com/microcosm-cc/bluemonday"
)

var policy = bluemonday.UGCPolicy()

var reviewTmpl = template.Must(template.New("review").Parse(
	`<article class="review"><h3>{{.Title}}</h3><div class="body">{{.Body}}</div></article>`))

func ReviewPreview(w http.ResponseWriter, r *http.Request) {
	title := r.PostFormValue("title")
	body := policy.Sanitize(r.PostFormValue("body"))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	reviewTmpl.Execute(w, struct {
		Title string
		Body  template.HTML
	}{title, template.HTML(body)})
}
