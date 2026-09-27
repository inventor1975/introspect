package profile

import (
	"encoding/base64"
	"encoding/json"
	"net/http"
	"os"
	"path/filepath"
)

type previewRequest struct {
	UserID int    `json:"user_id"`
	Avatar string `json:"avatar"`
}

type previewResponse struct {
	UserID int    `json:"user_id"`
	Image  string `json:"image"`
}

type Handler struct {
	MediaDir string
}

func (h Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	var req previewRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid json", http.StatusBadRequest)
		return
	}
	raw, err := os.ReadFile(filepath.Join(h.MediaDir, req.Avatar))
	if err != nil {
		http.Error(w, "avatar missing", http.StatusNotFound)
		return
	}
	resp := previewResponse{UserID: req.UserID, Image: base64.StdEncoding.EncodeToString(raw)}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}
