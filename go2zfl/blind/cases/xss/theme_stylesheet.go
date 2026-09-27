package themestylesheet

import (
	"fmt"
	"net/http"
)

var allowedThemes = map[string]bool{
	"light":    true,
	"dark":     true,
	"solarize": true,
}

func ThemedPage(w http.ResponseWriter, r *http.Request) {
	theme := r.URL.Query().Get("theme")
	if !allowedThemes[theme] {
		theme = "light"
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<html><head><link rel="stylesheet" href="/static/themes/%s.css"></head>
<body class="theme-%s"><h1>Dashboard</h1></body></html>`, theme, theme)
}
