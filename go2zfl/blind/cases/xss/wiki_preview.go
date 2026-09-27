package wikipreview

import (
	"net/http"

	"github.com/russross/blackfriday/v2"
)

func PreviewPage(w http.ResponseWriter, r *http.Request) {
	src := r.PostFormValue("source")
	rendered := blackfriday.Run([]byte(src))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Write([]byte("<div class=\"wiki-preview\">"))
	w.Write(rendered)
	w.Write([]byte("</div>"))
}
