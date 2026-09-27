package devices

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
)

type Device struct {
	Serial   string `db:"serial" json:"serial"`
	Owner    string `db:"owner" json:"owner"`
	Firmware string `db:"firmware" json:"firmware"`
}

type DeviceAPI struct {
	DB *sqlx.DB
}

func (d *DeviceAPI) Current(c *gin.Context) {
	serial := c.GetHeader("X-Device-Serial")
	if serial == "" {
		c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "device header missing"})
		return
	}

	var dev Device
	q := fmt.Sprintf("SELECT serial, owner, firmware FROM devices WHERE serial = '%s'", serial)
	if err := d.DB.Get(&dev, q); err != nil {
		c.AbortWithStatusJSON(http.StatusNotFound, gin.H{"error": "unknown device"})
		return
	}
	c.JSON(http.StatusOK, dev)
}
