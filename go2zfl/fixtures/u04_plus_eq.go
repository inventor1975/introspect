package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) {
  c := "ls "
  c += r.FormValue("c")
  exec.Command("sh", "-c", c).Run() } // REFUTED
