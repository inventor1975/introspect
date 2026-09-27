package shortlinks

import (
	"database/sql"
	"net/http"
	"net/url"
)

type Shortener struct {
	DB   *sql.DB
	Base string
}

func (s *Shortener) Resolve(w http.ResponseWriter, r *http.Request) {
	code := r.URL.Query().Get("c")
	campaign := r.URL.Query().Get("utm_campaign")

	var target string
	if err := s.DB.QueryRow("SELECT target FROM links WHERE code = ?", code).Scan(&target); err != nil {
		http.NotFound(w, r)
		return
	}

	u, err := url.Parse(target)
	if err != nil {
		http.Error(w, "bad target", http.StatusInternalServerError)
		return
	}
	q := u.Query()
	if campaign != "" {
		q.Set("utm_campaign", campaign)
	}
	u.RawQuery = q.Encode()

	if _, err := s.DB.Exec("UPDATE links SET hits = hits + 1 WHERE code = ?", code); err != nil {
		http.Error(w, "update failed", http.StatusInternalServerError)
		return
	}
	http.Redirect(w, r, u.String(), http.StatusFound)
}
