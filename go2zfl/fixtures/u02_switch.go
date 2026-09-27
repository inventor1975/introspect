package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) {
  c := "ls"
  switch r.FormValue("m") { case "a": c = r.FormValue("c"); case "b": c = "pwd" }
  exec.Command("sh", "-c", c).Run() } // REFUTED
