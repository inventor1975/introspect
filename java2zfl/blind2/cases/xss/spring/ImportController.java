package blind2.xss.spring;

import org.owasp.encoder.Encode;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ImportController {

    @PostMapping(value = "/imports/confirm", produces = "text/html")
    public String confirm(@RequestParam("label") String label, @RequestParam("rows") String rows) {
        try {
            int count = Integer.parseInt(rows);
            return "<p>Importing " + count + " rows into <b>" + Encode.forHtml(label) + "</b>.</p>";
        } catch (NumberFormatException e) {
            return "<p class=\"error\">Row count must be a number (got " + rows + ") for " + Encode.forHtml(label) + ".</p>";
        }
    }
}
