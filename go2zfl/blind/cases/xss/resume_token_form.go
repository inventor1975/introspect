package resumetoken

import (
	"encoding/base64"
	"io"
	"net/http"
)

func ResumeForm(w http.ResponseWriter, r *http.Request) {
	state := r.FormValue("state")
	token := base64.RawURLEncoding.EncodeToString([]byte(state))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, `<form method="post" action="/wizard/resume">`)
	io.WriteString(w, `<input type="hidden" name="token" value="`+token+`">`)
	io.WriteString(w, `<button>Continue</button></form>`)
}
