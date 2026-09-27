package docspreview

import (
	"net/http"

	"github.com/microcosm-cc/bluemonday"
	"github.com/russross/blackfriday/v2"
)

func PreviewDoc(w http.ResponseWriter, r *http.Request) {
	src := r.PostFormValue("markdown")
	unsafe := blackfriday.Run([]byte(src))
	clean := bluemonday.UGCPolicy().SanitizeBytes(unsafe)

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write([]byte("<div class=\"doc-preview\">"))
	w.Write(clean)
	w.Write([]byte("</div>"))
}
