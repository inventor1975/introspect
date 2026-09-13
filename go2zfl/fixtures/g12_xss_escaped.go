package main
import ("net/http"; "html")
func esc(w http.ResponseWriter, r *http.Request) {
	q := r.FormValue("q")
	w.Write([]byte(html.EscapeString(q)))   // clean: escaped for xss
	w.Write([]byte(q))                       // EXPECT: REFUTED [xss]
}
