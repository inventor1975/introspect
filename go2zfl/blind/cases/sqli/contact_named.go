package contacts

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
)

type Contact struct {
	Name    string `db:"name" json:"name" form:"name"`
	Email   string `db:"email" json:"email" form:"email"`
	Company string `db:"company" json:"company" form:"company"`
	Note    string `db:"note" json:"note" form:"note"`
}

type ContactAPI struct {
	DB *sqlx.DB
}

func (a *ContactAPI) Create(c *gin.Context) {
	var ct Contact
	if err := c.ShouldBind(&ct); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err := a.DB.NamedExec(`INSERT INTO contacts (name, email, company, note)
		VALUES (:name, :email, :company, :note)`, ct)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "insert failed"})
		return
	}
	c.JSON(http.StatusCreated, ct)
}
