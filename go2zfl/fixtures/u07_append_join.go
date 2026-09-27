package main
import ("net/http"; "os/exec"; "strings"; "strconv"; "somelib")
func handler(w http.ResponseWriter, r *http.Request) {
  args := []string{"ls"}
  args = append(args, r.FormValue("c"))
  exec.Command("sh", "-c", strings.Join(args, " ")).Run() } // REFUTED
