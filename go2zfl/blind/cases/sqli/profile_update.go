package profile

import (
	"database/sql"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type updateProfileInput struct {
	DisplayName string `json:"display_name" binding:"required"`
	Bio         string `json:"bio"`
}

type ProfileController struct {
	DB *sql.DB
}

func (pc *ProfileController) Update(c *gin.Context) {
	userID := c.GetInt64("user_id")

	var in updateProfileInput
	if err := c.ShouldBindJSON(&in); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	stmt := fmt.Sprintf("UPDATE profiles SET display_name = '%s', bio = '%s' WHERE user_id = %d",
		in.DisplayName, in.Bio, userID)
	if _, err := pc.DB.Exec(stmt); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "update failed"})
		return
	}
	c.Status(http.StatusNoContent)
}

func (pc *ProfileController) Register(r *gin.RouterGroup) {
	r.PUT("/profile", pc.Update)
}
