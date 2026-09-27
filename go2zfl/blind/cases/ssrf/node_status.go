package nodestatus

import (
	"encoding/json"
	"net/http"
	"net/url"

	"github.com/gorilla/mux"
)

type nodeInfo struct {
	Version string `json:"version"`
	Uptime  int64  `json:"uptime"`
}

func NodeStatus(w http.ResponseWriter, r *http.Request) {
	u := url.URL{
		Scheme: "http",
		Host:   r.FormValue("node"),
		Path:   "/admin/status",
	}
	resp, err := http.Get(u.String())
	if err != nil {
		w.WriteHeader(http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var info nodeInfo
	json.NewDecoder(resp.Body).Decode(&info)
	json.NewEncoder(w).Encode(info)
}

func Attach(r *mux.Router) {
	r.Path("/cluster/node").HandlerFunc(NodeStatus)
}
