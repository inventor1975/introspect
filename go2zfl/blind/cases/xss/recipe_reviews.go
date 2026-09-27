package recipereviews

import (
	"database/sql"
	"html/template"
	"net/http"
)

type Review struct {
	Author string
	Body   template.HTML
}

type Handler struct {
	DB   *sql.DB
	Tmpl *template.Template
}

func (h *Handler) PostReview(w http.ResponseWriter, r *http.Request) {
	recipeID := r.FormValue("recipe_id")
	_, err := h.DB.Exec(
		"INSERT INTO reviews (recipe_id, author, body) VALUES ($1, $2, $3)",
		recipeID, r.FormValue("author"), r.FormValue("body"),
	)
	if err != nil {
		http.Error(w, "could not save review", http.StatusInternalServerError)
		return
	}
	http.Redirect(w, r, "/recipes/reviews?recipe_id="+recipeID, http.StatusSeeOther)
}

func (h *Handler) ListReviews(w http.ResponseWriter, r *http.Request) {
	rows, err := h.DB.Query("SELECT author, body FROM reviews WHERE recipe_id = $1", r.FormValue("recipe_id"))
	if err != nil {
		http.Error(w, "db error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var reviews []Review
	for rows.Next() {
		var author, body string
		if err := rows.Scan(&author, &body); err != nil {
			continue
		}
		reviews = append(reviews, Review{Author: author, Body: template.HTML(body)})
	}
	h.Tmpl.ExecuteTemplate(w, "reviews.html", reviews)
}
