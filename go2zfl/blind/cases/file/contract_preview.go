package contracts

import (
	"net/http"
	"os"

	"example.com/docportal/lib/pathutil"
)

var previewDir = "/srv/docportal/contracts/previews"

func PreviewContract(w http.ResponseWriter, r *http.Request) {
	doc := r.URL.Query().Get("doc")
	full, err := pathutil.Contained(previewDir, doc)
	if err != nil {
		http.Error(w, "invalid document", http.StatusBadRequest)
		return
	}
	data, err := os.ReadFile(full)
	if err != nil {
		http.Error(w, "preview not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "image/png")
	w.Write(data)
}
