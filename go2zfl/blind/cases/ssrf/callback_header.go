package callbackheader

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

type Export struct {
	ID     string `json:"id"`
	Status string `json:"status"`
}

var notifier = &http.Client{Timeout: 5 * time.Second}

func StartExport(w http.ResponseWriter, r *http.Request) {
	exportID := mux.Vars(r)["id"]
	notifyURL := r.Header.Get("X-Callback-Url")
	w.WriteHeader(http.StatusAccepted)

	payload, _ := json.Marshal(Export{ID: exportID, Status: "queued"})
	if notifyURL != "" {
		req, err := http.NewRequest(http.MethodPost, notifyURL, bytes.NewBuffer(payload))
		if err != nil {
			log.Printf("export %s: bad callback: %v", exportID, err)
			return
		}
		req.Header.Set("Content-Type", "application/json")
		if resp, err := notifier.Do(req); err == nil {
			resp.Body.Close()
		}
	}
}

func Mount(r *mux.Router) {
	r.HandleFunc("/exports/{id}", StartExport).Methods(http.MethodPost)
}
