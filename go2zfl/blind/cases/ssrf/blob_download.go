package blobdownload

import (
	"io"
	"net/http"
	"regexp"

	"github.com/gin-gonic/gin"
)

var blobID = regexp.MustCompile(`^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`)

func Blob(c *gin.Context) {
	id := c.Param("id")
	if !blobID.MatchString(id) {
		c.AbortWithStatus(http.StatusNotFound)
		return
	}
	resp, err := http.Get("http://blobstore.internal:9090/blobs/" + id)
	if err != nil {
		c.AbortWithStatus(http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	c.Header("Content-Disposition", "attachment")
	c.Status(resp.StatusCode)
	io.Copy(c.Writer, resp.Body)
}
