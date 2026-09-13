package main
import ("net/http"; "os/exec")
var allow = map[string]bool{"ls": true, "pwd": true}
func gneg(w http.ResponseWriter, r *http.Request) {
	cmd := r.FormValue("cmd")
	if _, ok := allow[cmd]; !ok {            // negated map-membership guard
		return
	}
	exec.Command("sh", "-c", cmd)            // EXPECT: nothing (validated by the guard above)
}
