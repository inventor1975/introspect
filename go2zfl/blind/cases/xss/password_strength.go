package passwordstrength

import (
	"fmt"
	"log"
	"net/http"
	"unicode"
	"unicode/utf8"
)

func StrengthMeter(w http.ResponseWriter, r *http.Request) {
	pw := r.PostFormValue("password")
	log.Printf("strength check from %s", r.RemoteAddr)

	length := utf8.RuneCountInString(pw)
	classes := 0
	var hasUpper, hasDigit, hasSymbol bool
	for _, c := range pw {
		switch {
		case unicode.IsUpper(c):
			hasUpper = true
		case unicode.IsDigit(c):
			hasDigit = true
		case unicode.IsPunct(c) || unicode.IsSymbol(c):
			hasSymbol = true
		}
	}
	for _, b := range []bool{hasUpper, hasDigit, hasSymbol} {
		if b {
			classes++
		}
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<meter min=\"0\" max=\"4\" value=\"%d\"></meter><span>%d characters</span>", classes, length)
}
