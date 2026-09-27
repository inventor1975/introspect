package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) { exec.Command("sh", "-c", outer(r.FormValue("c"))).Run() }
func outer(v string) string { return inner(v) }
func inner(v string) string { return v } // REFUTED
