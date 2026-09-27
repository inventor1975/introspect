package couponcheck

import (
	"io"
	"net/http"
	"regexp"
)

var codePattern = regexp.MustCompile(`[A-Z0-9]{6}`)

func CheckCoupon(w http.ResponseWriter, r *http.Request) {
	code := r.FormValue("code")
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if !codePattern.MatchString(code) {
		io.WriteString(w, "<p class=\"error\">That does not look like a coupon code.</p>")
		return
	}
	io.WriteString(w, "<p>Coupon <strong>"+code+"</strong> has been applied.</p>")
}
