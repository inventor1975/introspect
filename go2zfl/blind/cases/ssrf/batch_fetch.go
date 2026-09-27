package batchfetch

import (
	"encoding/json"
	"net/http"
	"strings"
	"sync"
)

type result struct {
	URL    string `json:"url"`
	Status int    `json:"status"`
}

func fetchAll(urls []string) []result {
	out := make([]result, len(urls))
	var wg sync.WaitGroup
	for i, u := range urls {
		wg.Add(1)
		go func(i int, u string) {
			defer wg.Done()
			out[i] = result{URL: u}
			resp, err := http.Get(u)
			if err != nil {
				return
			}
			out[i].Status = resp.StatusCode
			resp.Body.Close()
		}(i, u)
	}
	wg.Wait()
	return out
}

func CheckLinks(w http.ResponseWriter, r *http.Request) {
	list := r.URL.Query().Get("links")
	var urls []string
	for _, part := range strings.Split(list, ",") {
		if p := strings.TrimSpace(part); p != "" {
			urls = append(urls, p)
		}
	}
	if len(urls) > 20 {
		urls = urls[:20]
	}
	json.NewEncoder(w).Encode(fetchAll(urls))
}
