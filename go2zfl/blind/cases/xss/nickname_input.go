package nicknameinput

import (
	"fmt"
	"net/http"

	"blindcases/xss/lib/pagekit"
)

func EditNickname(w http.ResponseWriter, r *http.Request) {
	nick := pagekit.StripAngles(r.FormValue("nick"))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<form method="post" action="/nickname">
<input type="text" name="nick" value="%s">
<button type="submit">Save</button>
</form>`, nick)
}
