package accounts

import (
	"io"
	"net/http"
	"os"
	"path/filepath"
)

const avatarDir = "./data/avatars"

// UploadAvatar saves the uploaded picture under the member's user name.
func UploadAvatar(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseMultipartForm(4 << 20); err != nil {
		http.Error(w, "upload too large", http.StatusRequestEntityTooLarge)
		return
	}
	user := r.FormValue("username")
	src, _, err := r.FormFile("avatar")
	if err != nil {
		http.Error(w, "no file", http.StatusBadRequest)
		return
	}
	defer src.Close()

	dst, err := os.Create(filepath.Join(avatarDir, user+".png"))
	if err != nil {
		http.Error(w, "cannot store avatar", http.StatusInternalServerError)
		return
	}
	defer dst.Close()
	if _, err := io.Copy(dst, src); err != nil {
		http.Error(w, "write failed", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusCreated)
}
