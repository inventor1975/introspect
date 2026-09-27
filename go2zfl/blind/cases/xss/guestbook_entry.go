package guestbook

import (
	"fmt"
	"net/http"
	"strings"
)

func cleanMessage(s string) string {
	s = strings.ReplaceAll(s, "<script>", "")
	s = strings.ReplaceAll(s, "</script>", "")
	s = strings.ReplaceAll(s, "javascript:", "")
	return s
}

func SignHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	author := cleanMessage(r.PostFormValue("author"))
	message := cleanMessage(r.PostFormValue("message"))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<article><h3>%s wrote:</h3><p>%s</p></article>", author, message)
}
