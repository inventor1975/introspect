package noticefragment

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func noticeFragment(c *gin.Context) {
	msg := c.DefaultQuery("msg", "Saved")
	level := c.DefaultQuery("level", "info")
	body := "<div class=\"alert alert-" + level + "\">" + msg + "</div>"
	c.Data(http.StatusOK, "text/html; charset=utf-8", []byte(body))
}

func Setup(r *gin.Engine) {
	r.GET("/fragments/notice", noticeFragment)
}
