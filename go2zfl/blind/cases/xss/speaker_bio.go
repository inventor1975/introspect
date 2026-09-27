package speakerbio

import (
	"html/template"
	"net/http"
)

var speakerTmpl = template.Must(template.New("speaker").Parse(`<html><body>
<div class="speaker" data-name="{{.Name}}">
  <h1>{{.Name}}</h1>
  <p class="bio">{{.Bio}}</p>
  <img src="/avatars/{{.Handle}}.png" alt="{{.Name}}">
</div>
</body></html>`))

type speaker struct {
	Name   string
	Handle string
	Bio    string
}

func SpeakerPreview(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	s := speaker{
		Name:   r.PostForm.Get("name"),
		Handle: r.PostForm.Get("handle"),
		Bio:    r.PostForm.Get("bio"),
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := speakerTmpl.Execute(w, s); err != nil {
		http.Error(w, "render error", http.StatusInternalServerError)
	}
}
