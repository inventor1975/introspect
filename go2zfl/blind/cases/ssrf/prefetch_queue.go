package prefetchqueue

import (
	"io"
	"log"
	"net/http"
	"sync"
	"time"
)

var (
	mu      sync.Mutex
	pending []string
	cache   = map[string][]byte{}
)

func Enqueue(w http.ResponseWriter, r *http.Request) {
	u := r.PostFormValue("resource")
	mu.Lock()
	pending = append(pending, u)
	mu.Unlock()
	w.WriteHeader(http.StatusAccepted)
}

func drain() {
	mu.Lock()
	batch := pending
	pending = nil
	mu.Unlock()
	for _, u := range batch {
		resp, err := http.Get(u)
		if err != nil {
			log.Printf("prefetch %s: %v", u, err)
			continue
		}
		body, _ := io.ReadAll(resp.Body)
		resp.Body.Close()
		mu.Lock()
		cache[u] = body
		mu.Unlock()
	}
}

func StartWorker() {
	go func() {
		for range time.Tick(30 * time.Second) {
			drain()
		}
	}()
}

func Register(mux *http.ServeMux) {
	mux.HandleFunc("/prefetch", Enqueue)
	StartWorker()
}
