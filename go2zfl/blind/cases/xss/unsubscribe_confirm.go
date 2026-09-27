package unsubscribe

import (
	"fmt"
	"net/http"
)

const pageHead = `<!DOCTYPE html>
<html>
<head><title>Unsubscribed</title></head>
<body>`

func Confirm(w http.ResponseWriter, r *http.Request) {
	email := r.URL.Query().Get("email")
	fmt.Fprint(w, pageHead)
	fmt.Fprintf(w, "<p>%s has been removed from the mailing list.</p>", email)
	fmt.Fprint(w, "</body></html>")
}
