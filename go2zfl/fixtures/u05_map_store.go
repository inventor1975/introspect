package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) {
  m := map[string]string{}
  m["c"] = r.FormValue("c")
  exec.Command("sh", "-c", m["c"]).Run() } // REFUTED
