package billingsync

import (
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/gorilla/mux"
)

func SyncCustomer(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(mux.Vars(r)["customer"], 10, 64)
	if err != nil {
		http.Error(w, "bad customer id", http.StatusBadRequest)
		return
	}
	base := os.Getenv("BILLING_API_URL")
	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("%s/customers/%d/sync", base, id), nil)
	if err != nil {
		http.Error(w, "misconfigured", http.StatusInternalServerError)
		return
	}
	req.Header.Set("Authorization", "Bearer "+os.Getenv("BILLING_API_TOKEN"))
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		http.Error(w, "billing unavailable", http.StatusBadGateway)
		return
	}
	resp.Body.Close()
	w.WriteHeader(resp.StatusCode)
}
