package authorbio

import (
	"html/template"
	"net/http"
)

var bioPage = template.Must(template.New("bio").Parse(`<html><body>
<h1>{{.Name}}</h1>
<div class="bio">{{.Bio}}</div>
</body></html>`))

type bioData struct {
	Name string
	Bio  template.HTML
}

func PreviewBio(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "bad form", http.StatusBadRequest)
		return
	}
	data := bioData{
		Name: r.PostFormValue("name"),
		Bio:  template.HTML(r.PostFormValue("bio")),
	}
	bioPage.Execute(w, data)
}
