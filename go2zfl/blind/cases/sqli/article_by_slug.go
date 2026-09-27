package articles

import (
	"database/sql"
	"fmt"
	"html/template"
	"net/http"

	"github.com/gorilla/mux"
)

type App struct {
	DB   *sql.DB
	Tmpl *template.Template
}

type Article struct {
	Title string
	Body  string
}

func (a *App) ShowArticle(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	slug := vars["slug"]

	var art Article
	q := fmt.Sprintf(`SELECT title, body FROM articles WHERE slug = '%s' AND published = 1`, slug)
	err := a.DB.QueryRow(q).Scan(&art.Title, &art.Body)
	if err == sql.ErrNoRows {
		http.NotFound(w, r)
		return
	}
	if err != nil {
		http.Error(w, "internal error", http.StatusInternalServerError)
		return
	}
	a.Tmpl.ExecuteTemplate(w, "article.html", art)
}

func (a *App) Router() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/articles/{slug}", a.ShowArticle).Methods("GET")
	return r
}
