package webhookstore

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type Hooks struct {
	DB     *sql.DB
	Client *http.Client
}

func (h *Hooks) Register(c *gin.Context) {
	accountID := c.GetString("account_id")
	target := c.PostForm("url")
	_, err := h.DB.ExecContext(c, "INSERT INTO webhooks(account_id, url, created_at) VALUES ($1, $2, $3)",
		accountID, target, time.Now())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not save"})
		return
	}
	c.Status(http.StatusCreated)
}

func (h *Hooks) Deliver(c *gin.Context) {
	accountID := c.GetString("account_id")
	rows, err := h.DB.QueryContext(c, "SELECT url FROM webhooks WHERE account_id = $1", accountID)
	if err != nil {
		c.Status(http.StatusInternalServerError)
		return
	}
	defer rows.Close()
	event, _ := json.Marshal(gin.H{"type": "order.updated", "at": time.Now().Unix()})
	delivered := 0
	for rows.Next() {
		var hookURL string
		if err := rows.Scan(&hookURL); err != nil {
			continue
		}
		resp, err := h.Client.Post(hookURL, "application/json", bytes.NewReader(event))
		if err == nil {
			resp.Body.Close()
			delivered++
		}
	}
	c.JSON(http.StatusOK, gin.H{"delivered": delivered})
}

func (h *Hooks) Routes(r *gin.Engine) {
	r.POST("/webhooks", h.Register)
	r.POST("/webhooks/test", h.Deliver)
}
