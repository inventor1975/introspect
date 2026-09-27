package blind.xss.reports;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.util.HtmlUtils;

/** Base class for the small reporting controllers that answer with a bare HTML page. */
public abstract class HtmlControllerSupport {

    protected ResponseEntity<String> html(String body) {
        String page = "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
                + "<link rel=\"stylesheet\" href=\"/static/reports.css\"></head><body>" + body + "</body></html>";
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(page);
    }

    protected String escaped(String value) {
        return value == null ? "" : HtmlUtils.htmlEscape(value);
    }
}
