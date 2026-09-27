package githubuser

import (
	"encoding/json"
	"net/http"
	"net/url"

	"github.com/gorilla/mux"
)

type ghUser struct {
	Login     string `json:"login"`
	AvatarURL string `json:"avatar_url"`
	Repos     int    `json:"public_repos"`
}

func GitHubUser(w http.ResponseWriter, r *http.Request) {
	username := mux.Vars(r)["username"]
	endpoint := url.URL{
		Scheme: "https",
		Host:   "api.github.com",
		Path:   "/users/" + username,
	}
	req, _ := http.NewRequestWithContext(r.Context(), http.MethodGet, endpoint.String(), nil)
	req.Header.Set("Accept", "application/vnd.github+json")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		http.Error(w, "github unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var u ghUser
	json.NewDecoder(resp.Body).Decode(&u)
	json.NewEncoder(w).Encode(u)
}

func Routes(r *mux.Router) {
	r.HandleFunc("/gh/{username}", GitHubUser).Methods("GET")
}
