package fx

import (
	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	"gorm.io/gorm"
)

type Item struct{ Name string }

func Find(c *gin.Context, db *gorm.DB, x *sqlx.DB) {
	name := c.Query("name")
	var items []Item
	db.Where("name = '" + name + "'").Find(&items)
	db.Where(map[string]interface{}{"name": name}).Find(&items) // a map condition is bound
	var it Item
	x.Get(&it, "SELECT * FROM items WHERE name = '"+name+"'")
	c.JSON(200, items)
}
