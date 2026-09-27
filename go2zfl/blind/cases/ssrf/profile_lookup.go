package profilelookup

import (
	"encoding/json"
	"net/http"
	"net/url"
	"time"
)

var directory = &http.Client{Timeout: 3 * time.Second}

type Profile struct {
	Login string `json:"login"`
	Name  string `json:"name"`
	Team  string `json:"team"`
}

func GetProfile(w http.ResponseWriter, r *http.Request) {
	login := r.FormValue("login")
	endpoint := "https://directory.corp.acme.io/people/" + url.PathEscape(login) + "/card"
	resp, err := directory.Get(endpoint)
	if err != nil {
		http.Error(w, "directory offline", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var p Profile
	if err := json.NewDecoder(resp.Body).Decode(&p); err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(p)
}
