package tenants

import (
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

const tenantsRoot = "/srv/tenants"

type ctxKey string

const tenantKey ctxKey = "tenant"

func tenantFromContext(r *http.Request) int {
	id, _ := r.Context().Value(tenantKey).(int)
	return id
}

func ServeTenantFile(w http.ResponseWriter, r *http.Request) {
	base := filepath.Join(tenantsRoot, strconv.Itoa(tenantFromContext(r)))
	full := filepath.Join(base, r.URL.Query().Get("doc"))
	if !strings.HasPrefix(full, base) {
		http.Error(w, "access denied", http.StatusForbidden)
		return
	}
	data, err := os.ReadFile(full)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "application/octet-stream")
	w.Write(data)
}
