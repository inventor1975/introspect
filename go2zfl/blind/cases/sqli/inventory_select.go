package inventory

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
)

type Item struct {
	SKU      string `db:"sku" json:"sku"`
	Name     string `db:"name" json:"name"`
	Quantity int    `db:"quantity" json:"quantity"`
	Location string `db:"location" json:"location"`
}

type InventoryAPI struct {
	DB *sqlx.DB
}

func buildInventoryQuery(location, category string) string {
	var conds []string
	conds = append(conds, "quantity > 0")
	if location != "" {
		conds = append(conds, "location = '"+location+"'")
	}
	if category != "" {
		conds = append(conds, "category = '"+category+"'")
	}
	return "SELECT sku, name, quantity, location FROM items WHERE " + strings.Join(conds, " AND ")
}

func (api *InventoryAPI) InStock(c *gin.Context) {
	q := buildInventoryQuery(c.Query("location"), c.Query("category"))

	var items []Item
	if err := api.DB.Select(&items, q); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "lookup failed"})
		return
	}
	c.JSON(http.StatusOK, items)
}

func (api *InventoryAPI) Register(r *gin.Engine) {
	r.GET("/inventory/in-stock", api.InStock)
}
