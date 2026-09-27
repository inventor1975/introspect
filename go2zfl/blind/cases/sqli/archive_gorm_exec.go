package archive

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type ArchiveController struct {
	DB *gorm.DB
}

type archiveRequest struct {
	Project string `form:"project"`
	Before  string `form:"before"`
}

func (a *ArchiveController) ArchiveProject(c *gin.Context) {
	var req archiveRequest
	if err := c.ShouldBind(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err := a.DB.Transaction(func(tx *gorm.DB) error {
		copySQL := fmt.Sprintf("INSERT INTO tasks_archive SELECT * FROM tasks WHERE project = '%s' AND closed_at < '%s'", req.Project, req.Before)
		if err := tx.Exec(copySQL).Error; err != nil {
			return err
		}
		return tx.Exec("DELETE FROM tasks WHERE project = ? AND closed_at < ?", req.Project, req.Before).Error
	})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "archive failed"})
		return
	}
	c.Status(http.StatusAccepted)
}
