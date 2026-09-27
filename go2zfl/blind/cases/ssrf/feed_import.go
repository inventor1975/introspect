package feedimport

import (
	"encoding/json"
	"encoding/xml"
	"net/http"
)

type importRequest struct {
	FeedURL string `json:"feed_url"`
	Label   string `json:"label"`
}

type rss struct {
	Channel struct {
		Title string `xml:"title"`
		Items []struct {
			Title string `xml:"title"`
			Link  string `xml:"link"`
		} `xml:"item"`
	} `xml:"channel"`
}

func ImportFeed(w http.ResponseWriter, r *http.Request) {
	var in importRequest
	if err := json.NewDecoder(r.Body).Decode(&in); err != nil {
		http.Error(w, "invalid json", http.StatusBadRequest)
		return
	}
	resp, err := http.Get(in.FeedURL)
	if err != nil {
		http.Error(w, "could not load feed", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var doc rss
	if err := xml.NewDecoder(resp.Body).Decode(&doc); err != nil {
		http.Error(w, "not rss", http.StatusUnprocessableEntity)
		return
	}
	json.NewEncoder(w).Encode(map[string]interface{}{
		"label": in.Label,
		"title": doc.Channel.Title,
		"count": len(doc.Channel.Items),
	})
}
