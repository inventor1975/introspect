package uploads

import (
	"log"
	"net/http"
	"os"
	"path/filepath"
)

const (
	incomingDir = "/var/uploads/incoming"
	publishDir  = "/var/uploads/published"
)

func publishUpload(w http.ResponseWriter, r *http.Request) {
	tmpID := filepath.Base(r.PostFormValue("upload_id"))
	name := r.PostFormValue("filename")
	display := filepath.Base(name)
	log.Printf("publishing upload %s as %s", tmpID, display)

	src := filepath.Join(incomingDir, tmpID)
	dst := filepath.Join(publishDir, name)
	if err := os.Rename(src, dst); err != nil {
		http.Error(w, "publish failed", http.StatusInternalServerError)
		return
	}
	w.Write([]byte("published " + display))
}

func init() {
	http.HandleFunc("/uploads/publish", publishUpload)
}
