package partnerlink

import (
	"html/template"
	"net/http"
)

var linkTmpl = template.Must(template.New("partner").Parse(
	`<li class="partner"><a href="{{.URL}}" target="_blank" rel="noopener">{{.Label}}</a></li>`))

type partner struct {
	URL   string
	Label string
}

func PartnerLink(w http.ResponseWriter, r *http.Request) {
	p := partner{
		URL:   r.URL.Query().Get("url"),
		Label: r.URL.Query().Get("label"),
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	linkTmpl.Execute(w, p)
}
