package relativeresolve

import (
	"io"
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
)

var helpBase, _ = url.Parse("https://help-content.internal.acme.io/articles/")

func Article(c *gin.Context) {
	ref, err := url.Parse(c.Query("ref"))
	if err != nil {
		c.String(http.StatusBadRequest, "bad ref")
		return
	}
	target := helpBase.ResolveReference(ref)
	if target.Scheme != helpBase.Scheme || target.Host != helpBase.Host {
		c.String(http.StatusBadRequest, "ref must be relative to the help centre")
		return
	}
	resp, err := http.Get(target.String())
	if err != nil {
		c.String(http.StatusBadGateway, "article unavailable")
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	c.Data(http.StatusOK, "text/html; charset=utf-8", body)
}
