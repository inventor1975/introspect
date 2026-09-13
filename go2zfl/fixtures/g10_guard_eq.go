package main
import ("net/http"; "os/exec")
func geq(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("name")
	if name == "ls" {
		exec.Command("sh", "-c", name)     // EXPECT: nothing (equality guard narrows name)
	}
	exec.Command("sh", "-c", name)          // EXPECT: REFUTED [shell] (unguarded, name still tainted)
}
