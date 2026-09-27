package mailer

import (
	"html/template"
	"net/http"
	"path/filepath"

	"example.com/docportal/lib/pathutil"
	"github.com/gorilla/mux"
)

const templatesDir = "templates/mail"

type previewData struct {
	Recipient string
}

func previewMail(w http.ResponseWriter, r *http.Request) {
	name := pathutil.Normalize(r.FormValue("template"))
	tmpl, err := template.ParseFiles(filepath.Join(templatesDir, name))
	if err != nil {
		http.Error(w, "template error", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	tmpl.Execute(w, previewData{Recipient: "preview@example.com"})
}

func Routes() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/mail/preview", previewMail).Methods("GET", "POST")
	return r
}
