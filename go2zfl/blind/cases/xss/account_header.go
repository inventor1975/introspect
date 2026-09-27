package accountheader

import (
	"fmt"
	"net/http"

	"github.com/example-shop/platform/auth"
)

func AccountHeader(w http.ResponseWriter, r *http.Request) {
	user, ok := auth.UserFromContext(r.Context())
	if !ok {
		http.Redirect(w, r, "/login", http.StatusFound)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "<header><span class=\"hello\">Signed in as %s</span></header>", user.DisplayName)
}
