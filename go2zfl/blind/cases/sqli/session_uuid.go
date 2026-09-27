package sessions

import (
	"database/sql"
	"encoding/json"
	"net/http"

	"github.com/google/uuid"
	"github.com/gorilla/mux"
)

type SessionAPI struct {
	DB *sql.DB
}

func (s *SessionAPI) Get(w http.ResponseWriter, r *http.Request) {
	parsed, err := uuid.Parse(mux.Vars(r)["sid"])
	if err != nil {
		http.Error(w, "invalid session id", http.StatusBadRequest)
		return
	}
	sid := parsed.String()

	var userID int64
	var agent string
	q := "SELECT user_id, user_agent FROM sessions WHERE id = '" + sid + "' AND revoked = false"
	if err := s.DB.QueryRow(q).Scan(&userID, &agent); err != nil {
		http.NotFound(w, r)
		return
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"user_id": userID, "agent": agent})
}
