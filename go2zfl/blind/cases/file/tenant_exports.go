package tenants

import (
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

const exportsRoot = "/srv/tenant-exports"

type tenantCtxKey struct{}

func currentTenant(r *http.Request) (int, bool) {
	id, ok := r.Context().Value(tenantCtxKey{}).(int)
	return id, ok
}

func TenantExport(w http.ResponseWriter, r *http.Request) {
	tenant, ok := currentTenant(r)
	if !ok {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return
	}
	base := filepath.Clean(filepath.Join(exportsRoot, strconv.Itoa(tenant)))
	full := filepath.Join(base, r.URL.Query().Get("doc"))
	if !strings.HasPrefix(full, base+string(os.PathSeparator)) {
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
