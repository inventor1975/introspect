package supportticket

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type ticketForm struct {
	Subject  string `form:"subject" binding:"required,max=120"`
	Email    string `form:"email" binding:"required,email"`
	Priority string `form:"priority"`
}

func submitTicket(c *gin.Context) {
	var f ticketForm
	if err := c.ShouldBind(&f); err != nil {
		c.String(http.StatusBadRequest, "invalid ticket")
		return
	}
	c.Header("Content-Type", "text/html; charset=utf-8")
	c.Status(http.StatusCreated)
	c.Writer.WriteString("<p>Ticket created: <b>" + f.Subject + "</b></p>")
	c.Writer.WriteString("<p>We will reply to " + f.Email + "</p>")
}

func Register(r *gin.Engine) {
	r.POST("/support/tickets", submitTicket)
}
