package feeddefault

import (
	"encoding/json"
	"log"
	"net/http"
)

const newsFeed = "https://news.acme.io/feed.json"

type item struct {
	Title string `json:"title"`
	URL   string `json:"url"`
}

func Headlines(w http.ResponseWriter, r *http.Request) {
	feed := r.URL.Query().Get("feed")
	if feed != "" {
		log.Printf("headlines: ignoring custom feed request %q from %s", feed, r.RemoteAddr)
	}
	feed = newsFeed
	resp, err := http.Get(feed)
	if err != nil {
		http.Error(w, "feed unavailable", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var items []item
	json.NewDecoder(resp.Body).Decode(&items)
	json.NewEncoder(w).Encode(items)
}
