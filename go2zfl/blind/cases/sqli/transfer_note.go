package transfers

import (
	"database/sql"
	"net/http"

	"github.com/gorilla/mux"
)

type Bank struct {
	DB *sql.DB
}

func (b *Bank) AddNote(w http.ResponseWriter, r *http.Request) {
	transferID := mux.Vars(r)["id"]
	note := r.PostFormValue("note")

	tx, err := b.DB.Begin()
	if err != nil {
		http.Error(w, "tx failed", http.StatusInternalServerError)
		return
	}
	defer tx.Rollback()

	if _, err := tx.Exec("UPDATE transfers SET memo = '"+note+"' WHERE id = ?", transferID); err != nil {
		http.Error(w, "update failed", http.StatusInternalServerError)
		return
	}
	if _, err := tx.Exec("INSERT INTO transfer_history (transfer_id, kind) VALUES (?, 'note')", transferID); err != nil {
		http.Error(w, "history failed", http.StatusInternalServerError)
		return
	}
	if err := tx.Commit(); err != nil {
		http.Error(w, "commit failed", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (b *Bank) Routes(r *mux.Router) {
	r.HandleFunc("/transfers/{id}/note", b.AddNote).Methods("POST")
}
