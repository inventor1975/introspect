package prefs

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gorilla/mux"
	"github.com/gorilla/sessions"
)

var store = sessions.NewCookieStore([]byte(os.Getenv("SESSION_KEY")))

const avatarsDir = "/srv/app/avatars"

func savePreferences(w http.ResponseWriter, r *http.Request) {
	sess, _ := store.Get(r, "prefs")
	sess.Values["avatar"] = r.PostFormValue("avatar")
	sess.Values["lang"] = r.PostFormValue("lang")
	if err := sess.Save(r, w); err != nil {
		http.Error(w, "session error", http.StatusInternalServerError)
		return
	}
	http.Redirect(w, r, "/profile", http.StatusSeeOther)
}

func currentAvatar(w http.ResponseWriter, r *http.Request) {
	sess, _ := store.Get(r, "prefs")
	name, ok := sess.Values["avatar"].(string)
	if !ok || name == "" {
		name = "default.png"
	}
	img, err := os.ReadFile(filepath.Join(avatarsDir, name))
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "image/png")
	w.Write(img)
}

func Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/preferences", savePreferences).Methods("POST")
	r.HandleFunc("/me/avatar", currentAvatar).Methods("GET")
	return r
}
