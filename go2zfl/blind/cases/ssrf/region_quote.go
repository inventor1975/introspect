package regionquote

import (
	"io"
	"net/http"

	"github.com/gorilla/mux"
)

func Quote(w http.ResponseWriter, r *http.Request) {
	region := mux.Vars(r)["region"]
	var host string
	switch region {
	case "eu":
		host = "https://quotes.eu.acme.io"
	case "us":
		host = "https://quotes.us.acme.io"
	case "apac":
		host = "https://quotes.apac.acme.io"
	default:
		http.Error(w, "unsupported region", http.StatusBadRequest)
		return
	}
	resp, err := http.Post(host+"/v1/quote", "application/json", r.Body)
	if err != nil {
		http.Error(w, "quote service error", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)
}

func Routes(r *mux.Router) {
	r.HandleFunc("/quote/{region}", Quote).Methods(http.MethodPost)
}
