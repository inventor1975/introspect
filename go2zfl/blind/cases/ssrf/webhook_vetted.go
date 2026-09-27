package webhookvetted

import (
	"bytes"
	"database/sql"
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
)

var chatHosts = map[string]bool{
	"hooks.slack.com":    true,
	"discord.com":        true,
	"outlook.office.com": true,
}

type Notifier struct {
	DB *sql.DB
}

func (n *Notifier) SaveHook(c *gin.Context) {
	raw := c.PostForm("url")
	u, err := url.Parse(raw)
	if err != nil || u.Scheme != "https" || !chatHosts[u.Hostname()] || u.Port() != "" {
		c.JSON(http.StatusUnprocessableEntity, gin.H{"error": "only Slack, Discord or Teams webhooks are supported"})
		return
	}
	_, err = n.DB.Exec("UPDATE teams SET chat_hook = $1 WHERE id = $2", u.String(), c.GetInt64("team_id"))
	if err != nil {
		c.Status(http.StatusInternalServerError)
		return
	}
	c.Status(http.StatusNoContent)
}

func (n *Notifier) Announce(c *gin.Context) {
	var hook string
	err := n.DB.QueryRow("SELECT chat_hook FROM teams WHERE id = $1", c.GetInt64("team_id")).Scan(&hook)
	if err != nil || hook == "" {
		c.Status(http.StatusNotFound)
		return
	}
	body := bytes.NewBufferString(`{"text":"Deployment finished"}`)
	resp, err := http.Post(hook, "application/json", body)
	if err != nil {
		c.Status(http.StatusBadGateway)
		return
	}
	resp.Body.Close()
	c.Status(http.StatusOK)
}
