package main
import ("net/http"; "os/exec")
func h1(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("name")               // source
	exec.Command("sh", "-c", "echo "+name)     // EXPECT: REFUTED [shell]
}
