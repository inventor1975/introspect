package i18n

import (
	"io/fs"
	"net/http"
	"os"
)

type Bundles struct {
	fsys fs.FS
}

func NewBundles(dir string) *Bundles {
	return &Bundles{fsys: os.DirFS(dir)}
}

func (b *Bundles) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	lang := r.URL.Query().Get("lang")
	if lang == "" {
		lang = r.Header.Get("Accept-Language")
	}
	data, err := fs.ReadFile(b.fsys, lang+"/messages.json")
	if err != nil {
		data, err = fs.ReadFile(b.fsys, "en/messages.json")
		if err != nil {
			http.Error(w, "no bundle", http.StatusInternalServerError)
			return
		}
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(data)
}

func main() {
	http.Handle("/i18n/messages", NewBundles("/srv/app/locales"))
	http.ListenAndServe(":8082", nil)
}
