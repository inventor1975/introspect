package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) {
  var b strings.Builder
  b.WriteString("ls ")
  b.WriteString(r.FormValue("c"))
  exec.Command("sh", "-c", b.String()).Run() } // REFUTED
