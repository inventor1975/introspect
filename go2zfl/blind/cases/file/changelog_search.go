package releases

import (
	"bufio"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
)

const changelogPath = "/srv/app/CHANGELOG.md"

func searchChangelog(c *gin.Context) {
	q := strings.ToLower(c.Query("q"))
	f, err := os.Open(changelogPath)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "changelog unavailable"})
		return
	}
	defer f.Close()
	var hits []string
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		line := sc.Text()
		if q == "" || strings.Contains(strings.ToLower(line), q) {
			hits = append(hits, line)
		}
		if len(hits) >= 200 {
			break
		}
	}
	c.JSON(http.StatusOK, gin.H{"query": q, "lines": hits})
}

func Register(r *gin.Engine) {
	r.GET("/changelog/search", searchChangelog)
}
