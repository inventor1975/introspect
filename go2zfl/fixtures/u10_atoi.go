package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) {
  n, _ := strconv.Atoi(r.FormValue("n"))
  exec.Command("sh", "-c", "sleep " + strconv.Itoa(n)).Run() } // nothing
