package main
import ("os"; "net/http"; "os/exec"; "html/template"; "github.com/gin-gonic/gin")
func gmulti(c *gin.Context) {
	name := c.Query("name")            // gin source (receiver-typed; resolves c.Query vs db.Query)
	exec.Command("sh", "-c", name)      // EXPECT: REFUTED [shell]
	os.ReadFile("/data/" + name)        // EXPECT: REFUTED [file]
	http.Get("http://h/" + name)         // EXPECT: REFUTED [ssrf]
	_ = template.HTML(name)             // EXPECT: REFUTED [xss]
}
