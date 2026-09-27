package localegreeting

import (
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
)

type formatter func(name string) string

func greeterFor(lang string) formatter {
	switch lang {
	case "de":
		return func(n string) string { return fmt.Sprintf("<p>Hallo, %s!</p>", n) }
	case "fr":
		return func(n string) string { return fmt.Sprintf("<p>Bonjour, %s !</p>", n) }
	default:
		return func(n string) string { return fmt.Sprintf("<p>Hello, %s!</p>", n) }
	}
}

func makeGreetingHandler(site string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		greet := greeterFor(vars["lang"])
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		fmt.Fprintf(w, "<h1>%s</h1>%s", site, greet(r.URL.Query().Get("name")))
	}
}

func Routes(r *mux.Router) {
	r.HandleFunc("/{lang}/greeting", makeGreetingHandler("Acme Travel"))
}
