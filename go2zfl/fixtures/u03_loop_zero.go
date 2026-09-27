package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) {
  c := r.FormValue("c")
  for _, x := range []string{} { c = x }
  exec.Command("sh", "-c", c).Run() } // REFUTED
