package relativejoin

import (
	"io"
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
)

var apiBase, _ = url.Parse("https://docs-api.internal.acme.io/content/")

func Page(c *gin.Context) {
	ref, err := url.Parse(c.Query("ref"))
	if err != nil {
		c.String(http.StatusBadRequest, "bad ref")
		return
	}
	target := apiBase.ResolveReference(ref)
	resp, err := http.Get(target.String())
	if err != nil {
		c.String(http.StatusBadGateway, "content unavailable")
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	c.Data(http.StatusOK, "text/html; charset=utf-8", body)
}
