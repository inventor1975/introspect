package helpdesk

import (
	"database/sql"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
)

const attachmentsDir = "/var/helpdesk/attachments"

type AttachmentStore struct {
	DB *sql.DB
}

// Register records metadata for an attachment already uploaded to attachmentsDir.
func (s *AttachmentStore) Register(w http.ResponseWriter, r *http.Request) {
	ticket, err := strconv.Atoi(r.FormValue("ticket"))
	if err != nil {
		http.Error(w, "bad ticket", http.StatusBadRequest)
		return
	}
	stored := r.FormValue("stored_as")
	res, err := s.DB.Exec(`INSERT INTO attachments (ticket_id, stored_name) VALUES ($1, $2)`, ticket, stored)
	if err != nil {
		http.Error(w, "db error", http.StatusInternalServerError)
		return
	}
	id, _ := res.LastInsertId()
	w.Write([]byte(strconv.FormatInt(id, 10)))
}

// Download streams an attachment by its numeric id.
func (s *AttachmentStore) Download(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(r.URL.Query().Get("id"), 10, 64)
	if err != nil {
		http.Error(w, "bad id", http.StatusBadRequest)
		return
	}
	var storedName string
	err = s.DB.QueryRow(`SELECT stored_name FROM attachments WHERE id = $1`, id).Scan(&storedName)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	f, err := os.Open(filepath.Join(attachmentsDir, storedName))
	if err != nil {
		http.NotFound(w, r)
		return
	}
	defer f.Close()
	io.Copy(w, f)
}

func Routes(mux *http.ServeMux, s *AttachmentStore) {
	mux.HandleFunc("/attachments/register", s.Register)
	mux.HandleFunc("/attachments/download", s.Download)
}
