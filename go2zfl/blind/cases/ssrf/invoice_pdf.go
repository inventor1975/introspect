package invoicepdf

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"example.com/blindsvc/lib/fetch"
)

type renderer interface {
	Render(logo []byte, invoiceID string) ([]byte, error)
}

type Handler struct {
	PDF renderer
}

func (h *Handler) Invoice(c *gin.Context) {
	invoiceID := c.Param("id")
	logoURL := c.DefaultQuery("logo", "https://assets.acme-cdn.net/logo.png")
	logo, err := fetch.Download(c.Request.Context(), logoURL)
	if err != nil {
		c.String(http.StatusBadGateway, "logo unavailable")
		return
	}
	doc, err := h.PDF.Render(logo, invoiceID)
	if err != nil {
		c.String(http.StatusInternalServerError, "render failed")
		return
	}
	c.Data(http.StatusOK, "application/pdf", doc)
}

func (h *Handler) Mount(r *gin.Engine) {
	r.GET("/invoices/:id/pdf", h.Invoice)
}
