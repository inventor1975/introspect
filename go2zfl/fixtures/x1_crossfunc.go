package main
import ("net/http"; "os/exec")
func runCmd(c string) { exec.Command("sh", "-c", c) }   // param -> shell (summary)
func h5(w http.ResponseWriter, r *http.Request) {
	cmd := r.FormValue("cmd")
	runCmd(cmd)                                  // EXPECT: REFUTED (cross-func summary)
	runCmd("safe")                               // EXPECT: clean
}
