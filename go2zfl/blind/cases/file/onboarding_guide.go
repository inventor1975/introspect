package onboarding

import (
	"net/http"
	"os"
)

func guide(w http.ResponseWriter, r *http.Request) {
	lang := r.FormValue("lang")
	path := "content/guides/en.md"
	if lang == "de" {
		path = "content/guides/de.md"
	} else if lang == "fr" {
		path = "content/guides/fr.md"
	} else if lang == "es" {
		path = "content/guides/es.md"
	}
	md, err := os.ReadFile(path)
	if err != nil {
		http.Error(w, "guide unavailable for "+lang, http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/markdown; charset=utf-8")
	w.Write(md)
}

func init() {
	http.HandleFunc("/onboarding/guide", guide)
}
