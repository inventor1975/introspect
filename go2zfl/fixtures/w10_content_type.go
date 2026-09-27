package fx

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Plain(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	fmt.Fprintf(w, "you sent %s", r.FormValue("m"))
}

func Gin(c *gin.Context) {
	c.String(200, "echo %s", c.Query("m")) // gin sends text/plain
	c.Data(200, "text/html; charset=utf-8", []byte("<p>"+c.Query("m")+"</p>"))
}
