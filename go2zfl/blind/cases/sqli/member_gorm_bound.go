package membersbound

import (
	"encoding/json"
	"net/http"

	"gorm.io/gorm"
)

type Member struct {
	ID       uint   `json:"id"`
	Username string `json:"username"`
	Level    int    `json:"level"`
}

type Server struct {
	orm *gorm.DB
}

func (s *Server) lookupMember(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "bad form", http.StatusBadRequest)
		return
	}
	username := r.FormValue("username")
	cond := "username = ? AND deleted_at IS NULL"

	var m Member
	if err := s.orm.Where(cond, username).First(&m).Error; err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(m)
}
