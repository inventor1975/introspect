package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func h(p string, f bool) string { if f { return p }; p = "x"; return p }
func handler(w http.ResponseWriter, r *http.Request) { exec.Command("sh", "-c", h(r.FormValue("c"), true)).Run() } // REFUTED
