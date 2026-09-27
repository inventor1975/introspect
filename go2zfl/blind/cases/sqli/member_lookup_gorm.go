package members

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

	var m Member
	res := s.orm.Where("username = '" + username + "'").First(&m)
	if res.Error != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(m)
}

func (s *Server) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/members/lookup", s.lookupMember)
	return mux
}
