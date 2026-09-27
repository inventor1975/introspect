package vendorlink

import (
	"html/template"
	"net/http"
)

const cardSrc = `<div class="vendor">
  <span>{{.Name}}</span>
  <a href="{{.Site}}" rel="nofollow">Visit website</a>
</div>`

var card = template.Must(template.New("vendor").Parse(cardSrc))

type vendorCard struct {
	Name string
	Site template.URL
}

func VendorCard(w http.ResponseWriter, r *http.Request) {
	site := r.FormValue("website")
	card.Execute(w, vendorCard{
		Name: r.FormValue("name"),
		Site: template.URL(site),
	})
}
