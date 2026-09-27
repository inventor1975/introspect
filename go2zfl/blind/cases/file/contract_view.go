package contracts

import (
	"net/http"
	"os"

	"example.com/docportal/lib/pathutil"
)

var contractsDir = "/srv/docportal/contracts"

func ViewContract(w http.ResponseWriter, r *http.Request) {
	doc := r.URL.Query().Get("doc")
	data, err := os.ReadFile(pathutil.Under(contractsDir, doc))
	if err != nil {
		http.Error(w, "contract not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "application/pdf")
	w.Write(data)
}
