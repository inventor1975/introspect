package coupons

import (
	"database/sql"
	"net/http"

	"github.com/gin-gonic/gin"
)

type CouponService struct {
	DB *sql.DB
}

func (s *CouponService) Redeem(c *gin.Context) {
	code := c.PostForm("code")
	if len(code) == 0 || len(code) > 32 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid coupon code"})
		return
	}

	res, err := s.DB.Exec("UPDATE coupons SET redeemed = 1 WHERE code = '" + code + "' AND redeemed = 0")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "redeem failed"})
		return
	}
	n, _ := res.RowsAffected()
	if n == 0 {
		c.JSON(http.StatusConflict, gin.H{"error": "coupon already used or unknown"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"redeemed": code})
}

func (s *CouponService) Routes(r *gin.Engine) {
	r.POST("/coupons/redeem", s.Redeem)
}
