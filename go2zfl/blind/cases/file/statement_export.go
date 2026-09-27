package banking

import (
	"fmt"
	"net/http"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

const statementsRoot = "/srv/bank/statements"

func accountID(c *gin.Context) (int64, bool) {
	v, ok := c.Get("account_id")
	if !ok {
		return 0, false
	}
	id, ok := v.(int64)
	return id, ok
}

func exportStatement(c *gin.Context) {
	acct, ok := accountID(c)
	if !ok {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}
	var fname string
	switch c.DefaultQuery("format", "pdf") {
	case "pdf":
		fname = "statement.pdf"
	case "csv":
		fname = "statement.csv"
	case "mt940":
		fname = "statement.sta"
	default:
		c.JSON(http.StatusBadRequest, gin.H{"error": "unsupported format"})
		return
	}
	c.File(filepath.Join(statementsRoot, fmt.Sprintf("%d", acct), fname))
}

func Routes(g *gin.RouterGroup) {
	g.GET("/statements/export", exportStatement)
}
