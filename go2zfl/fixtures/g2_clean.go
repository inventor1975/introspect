package main
import ("net/http"; "os/exec")
func h2(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()                          // Values, NOT a string arg -> no collision
	_ = q
	exec.Command("ls", "-la")                   // constant args: EXPECT nothing
}
