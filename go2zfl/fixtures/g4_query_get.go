package main
import ("net/http"; "os/exec")
func h4(w http.ResponseWriter, r *http.Request) {
	cmd := r.URL.Query().Get("cmd")             // chain source
	exec.Command("bash", "-c", cmd)             // EXPECT: REFUTED [shell]
}
