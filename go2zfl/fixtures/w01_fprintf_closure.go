package fx

import (
	"fmt"
	"net/http"
)

// an inline handler (a function literal) writing request data with fmt.Fprintf
func Routes(mux *http.ServeMux) {
	mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
		name := r.FormValue("name")
		fmt.Fprintf(w, "<h1>Hello %s</h1>", name)
	})
}
