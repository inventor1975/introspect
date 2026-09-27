package tenantdomain

import (
	"encoding/json"
	"net/http"
	"net/url"
	"strings"

	"github.com/gorilla/mux"
)

const tenantZone = ".tenants.acme-cloud.net"

func tenantURL(raw string) (*url.URL, bool) {
	u, err := url.Parse(raw)
	if err != nil || u.Scheme != "https" || u.User != nil || u.Port() != "" {
		return nil, false
	}
	host := strings.ToLower(u.Hostname())
	if !strings.HasSuffix(host, tenantZone) || len(host) == len(tenantZone) {
		return nil, false
	}
	return u, true
}

func Manifest(w http.ResponseWriter, r *http.Request) {
	u, ok := tenantURL(r.URL.Query().Get("tenant_url"))
	if !ok {
		http.Error(w, "tenant url must be within the tenant zone", http.StatusBadRequest)
		return
	}
	u.Path = "/manifest.json"
	resp, err := http.Get(u.String())
	if err != nil {
		http.Error(w, "tenant offline", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	var m map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&m)
	json.NewEncoder(w).Encode(m)
}

func Routes(r *mux.Router) {
	r.HandleFunc("/tenant/manifest", Manifest)
}
