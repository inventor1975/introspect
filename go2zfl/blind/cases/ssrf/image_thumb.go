package imagethumb

import (
	"image"
	_ "image/jpeg"
	_ "image/png"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

var httpClient = &http.Client{Timeout: 8 * time.Second}

func Thumbnail(c *gin.Context) {
	imageURL := c.Query("image")
	req, err := http.NewRequest(http.MethodGet, imageURL, nil)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "bad image url"})
		return
	}
	req.Header.Set("Accept", "image/*")
	resp, err := httpClient.Do(req)
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "fetch failed"})
		return
	}
	defer resp.Body.Close()
	cfg, format, err := image.DecodeConfig(resp.Body)
	if err != nil {
		c.JSON(http.StatusUnprocessableEntity, gin.H{"error": "not an image"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"width": cfg.Width, "height": cfg.Height, "format": format})
}

func Routes(r *gin.Engine) {
	r.GET("/thumb", Thumbnail)
}
