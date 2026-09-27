package blind.xss.reports;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuditTrailController extends HtmlControllerSupport {

    @GetMapping("/reports/audit")
    public ResponseEntity<String> audit(@RequestParam("actor") String actor,
                                        @RequestParam(value = "days", defaultValue = "7") int days) {
        return html("<h2>Activity for " + actor + "</h2>"
                + "<p>Showing the last " + days + " days.</p>"
                + "<table id=\"audit\"></table>");
    }
}
