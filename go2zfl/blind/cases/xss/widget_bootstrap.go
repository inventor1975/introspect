package widgetbootstrap

import (
	"html/template"
	"net/http"
)

var page = template.Must(template.New("w").Parse(`<html><head>
<script>
  var widgetConfig = {{.Config}};
  initWidget(widgetConfig);
</script>
</head><body><div id="widget"></div></body></html>`))

func EmbedWidget(w http.ResponseWriter, r *http.Request) {
	cfg := r.URL.Query().Get("config")
	if cfg == "" {
		cfg = "{}"
	}
	page.Execute(w, map[string]interface{}{
		"Config": template.JS(cfg),
	})
}
