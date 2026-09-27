package chatwidget

import (
	"fmt"
	"html/template"
	"net/http"
)

func ChatWidget(w http.ResponseWriter, r *http.Request) {
	room := template.JSEscapeString(r.URL.Query().Get("room"))
	nick := template.JSEscapeString(r.URL.Query().Get("nick"))

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<div id="chat"></div>
<script>
  Chat.join('%s', "%s");
</script>`, room, nick)
}
