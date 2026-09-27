package mirrorprobe

import (
	"encoding/json"
	"net/http"
	"time"
)

type probeResult struct {
	URL     string `json:"url"`
	Status  int    `json:"status"`
	Latency int64  `json:"latency_ms"`
	Err     string `json:"error,omitempty"`
}

func ProbeMirrors(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "bad form", http.StatusBadRequest)
		return
	}
	client := &http.Client{Timeout: 3 * time.Second}
	var results []probeResult
	for _, m := range r.Form["mirror"] {
		start := time.Now()
		res := probeResult{URL: m}
		resp, err := client.Get(m + "/RELEASE")
		if err != nil {
			res.Err = err.Error()
		} else {
			res.Status = resp.StatusCode
			resp.Body.Close()
		}
		res.Latency = time.Since(start).Milliseconds()
		results = append(results, res)
	}
	json.NewEncoder(w).Encode(results)
}
