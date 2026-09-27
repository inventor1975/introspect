package themes

import (
	"archive/zip"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
)

const themesDir = "/srv/cms/themes/installed"

func extractTo(dest string, zf *zip.File) error {
	target := filepath.Join(dest, zf.Name)
	if !strings.HasPrefix(target, filepath.Clean(dest)+string(os.PathSeparator)) {
		return fmt.Errorf("illegal entry %q", zf.Name)
	}
	if zf.FileInfo().IsDir() {
		return os.MkdirAll(target, 0o755)
	}
	if err := os.MkdirAll(filepath.Dir(target), 0o755); err != nil {
		return err
	}
	rc, err := zf.Open()
	if err != nil {
		return err
	}
	defer rc.Close()
	out, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0o644)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = io.Copy(out, rc)
	return err
}

func importTheme(c *gin.Context) {
	fh, err := c.FormFile("theme")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "theme archive required"})
		return
	}
	f, err := fh.Open()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "unreadable upload"})
		return
	}
	defer f.Close()
	zr, err := zip.NewReader(f, fh.Size)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "not a zip"})
		return
	}
	for _, zf := range zr.File {
		if err := extractTo(themesDir, zf); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
	}
	c.JSON(http.StatusCreated, gin.H{"files": len(zr.File)})
}

func Register(r *gin.Engine) {
	r.POST("/admin/themes/import", importTheme)
}
