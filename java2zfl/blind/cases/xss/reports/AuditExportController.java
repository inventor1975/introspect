package blind.xss.reports;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuditExportController extends HtmlControllerSupport {

    @GetMapping("/reports/audit/export")
    public ResponseEntity<String> export(@RequestParam("actor") String actor,
                                         @RequestParam(value = "days", defaultValue = "30") int days) {
        return html("<h2>Export activity for " + escaped(actor) + "</h2>"
                + "<p>The export covers " + days + " days and will be e-mailed when ready.</p>");
    }
}
