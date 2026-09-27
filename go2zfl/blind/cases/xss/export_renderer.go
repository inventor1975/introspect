package exportrenderer

import (
	"fmt"
	"html"
	"io"
	"net/http"
	"strings"
)

type Renderer interface {
	Render(out io.Writer, rows []string)
}

type tableRenderer struct{}

func (tableRenderer) Render(out io.Writer, rows []string) {
	io.WriteString(out, "<table>")
	for _, row := range rows {
		fmt.Fprintf(out, "<tr><td>%s</td></tr>", html.EscapeString(row))
	}
	io.WriteString(out, "</table>")
}

type listRenderer struct{}

func (listRenderer) Render(out io.Writer, rows []string) {
	io.WriteString(out, "<ul>")
	for _, row := range rows {
		io.WriteString(out, "<li>"+html.EscapeString(row)+"</li>")
	}
	io.WriteString(out, "</ul>")
}

var renderers = map[string]Renderer{
	"table": tableRenderer{},
	"list":  listRenderer{},
}

func ExportPreview(w http.ResponseWriter, r *http.Request) {
	rend, ok := renderers[r.URL.Query().Get("layout")]
	if !ok {
		rend = listRenderer{}
	}
	rows := strings.Split(r.URL.Query().Get("rows"), "|")
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	rend.Render(w, rows)
}
