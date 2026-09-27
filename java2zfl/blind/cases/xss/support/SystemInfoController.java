package blind.xss.support;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SystemInfoController {

    @GetMapping(value = "/support/about", produces = MediaType.TEXT_HTML_VALUE)
    public String about(@RequestParam(value = "view", required = false) String view) {
        String version = System.getProperty("app.version", "dev");
        String host = System.getenv().getOrDefault("HOSTNAME", "unknown");
        StringBuilder html = new StringBuilder("<dl class=\"about\">");
        html.append("<dt>Version</dt><dd>").append(version).append("</dd>");
        if ("full".equals(view)) {
            html.append("<dt>Node</dt><dd>").append(host).append("</dd>");
            html.append("<dt>Java</dt><dd>").append(System.getProperty("java.version")).append("</dd>");
        }
        return html.append("</dl>").toString();
    }
}
