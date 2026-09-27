package storefront

import (
	"net/http"
	"os"
)

func themeStylesheet(w http.ResponseWriter, r *http.Request) {
	theme := "default"
	if c, err := r.Cookie("theme"); err == nil && c.Value != "" {
		theme = c.Value
	}
	css, err := os.ReadFile("themes/" + theme + "/style.css")
	if err != nil {
		css, _ = os.ReadFile("themes/default/style.css")
	}
	w.Header().Set("Content-Type", "text/css")
	w.Header().Set("Cache-Control", "max-age=300")
	w.Write(css)
}

func init() {
	http.HandleFunc("/assets/theme.css", themeStylesheet)
}
