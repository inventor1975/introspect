package feedback

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"github.com/gin-gonic/gin"
)

const inboxDir = "/var/feedback/inbox"

type feedbackForm struct {
	Email   string `form:"email"`
	Subject string `form:"subject"`
	Message string `form:"message"`
}

func randomSuffix() string {
	b := make([]byte, 6)
	rand.Read(b)
	return hex.EncodeToString(b)
}

func submit(c *gin.Context) {
	var f feedbackForm
	if err := c.ShouldBind(&f); err != nil {
		c.String(http.StatusBadRequest, "invalid form")
		return
	}
	name := fmt.Sprintf("%s-%s.txt", time.Now().UTC().Format("20060102T150405"), randomSuffix())
	content := fmt.Sprintf("From: %s\nSubject: %s\n\n%s\n", f.Email, f.Subject, f.Message)
	if err := os.WriteFile(filepath.Join(inboxDir, name), []byte(content), 0o640); err != nil {
		c.String(http.StatusInternalServerError, "could not store feedback")
		return
	}
	c.String(http.StatusAccepted, "thanks, reference "+name)
}

func Register(r *gin.Engine) {
	r.POST("/feedback", submit)
}
