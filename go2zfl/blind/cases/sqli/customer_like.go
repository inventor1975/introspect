package customerlike

import (
	"database/sql"
	"net/http"

	"github.com/gin-gonic/gin"
)

type Customer struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

type Handler struct {
	DB *sql.DB
}

func (h *Handler) Search(c *gin.Context) {
	term := c.Query("q")
	pattern := "%" + term + "%"
	query := "SELECT id, name, email FROM customers WHERE name LIKE ? OR email LIKE ? ORDER BY name LIMIT 50"

	rows, err := h.DB.Query(query, pattern, pattern)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "search failed"})
		return
	}
	defer rows.Close()

	result := []Customer{}
	for rows.Next() {
		var cu Customer
		if err := rows.Scan(&cu.ID, &cu.Name, &cu.Email); err == nil {
			result = append(result, cu)
		}
	}
	c.JSON(http.StatusOK, result)
}
