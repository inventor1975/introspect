package maintenancenotice

import (
	"net/http"
	"os"
)

func MaintenanceNotice(w http.ResponseWriter, r *http.Request) {
	path := os.Getenv("NOTICE_HTML_PATH")
	if path == "" {
		path = "/etc/shop/notice.html"
	}
	content, err := os.ReadFile(path)
	if err != nil {
		w.WriteHeader(http.StatusNoContent)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write([]byte("<aside class=\"notice\">"))
	w.Write(content)
	w.Write([]byte("</aside>"))
}
