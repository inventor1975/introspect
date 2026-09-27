package healthfanout

import (
	"encoding/json"
	"net/http"
	"strconv"
	"sync"
	"time"
)

var dependencies = []string{
	"http://auth.internal:8000/healthz",
	"http://orders.internal:8000/healthz",
	"http://payments.internal:8000/healthz",
}

func Readiness(w http.ResponseWriter, r *http.Request) {
	timeoutMs, err := strconv.Atoi(r.URL.Query().Get("timeout_ms"))
	if err != nil || timeoutMs <= 0 || timeoutMs > 5000 {
		timeoutMs = 1000
	}
	client := &http.Client{Timeout: time.Duration(timeoutMs) * time.Millisecond}
	status := make(map[string]bool, len(dependencies))
	var mu sync.Mutex
	var wg sync.WaitGroup
	for _, dep := range dependencies {
		wg.Add(1)
		go func(dep string) {
			defer wg.Done()
			resp, err := client.Get(dep)
			ok := err == nil && resp.StatusCode == http.StatusOK
			if err == nil {
				resp.Body.Close()
			}
			mu.Lock()
			status[dep] = ok
			mu.Unlock()
		}(dep)
	}
	wg.Wait()
	json.NewEncoder(w).Encode(status)
}
