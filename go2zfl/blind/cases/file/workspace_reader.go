package workspace

import (
	"io"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

type Reader struct {
	root *os.Root
}

func NewReader(dir string) (*Reader, error) {
	root, err := os.OpenRoot(dir)
	if err != nil {
		return nil, err
	}
	return &Reader{root: root}, nil
}

func (rd *Reader) File(c *gin.Context) {
	name := c.Query("file")
	f, err := rd.root.Open(name)
	if err != nil {
		c.AbortWithStatusJSON(http.StatusNotFound, gin.H{"error": "cannot open file"})
		return
	}
	defer f.Close()
	c.Header("Content-Type", "application/octet-stream")
	io.Copy(c.Writer, f)
}

func Setup(r *gin.Engine) error {
	rd, err := NewReader("/data/workspaces/shared")
	if err != nil {
		return err
	}
	r.GET("/workspace/file", rd.File)
	return nil
}
