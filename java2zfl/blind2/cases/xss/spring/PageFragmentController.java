package blind2.xss.spring;

import java.util.HashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PageFragmentController {

    @GetMapping(value = "/fragments/footer-note", produces = "text/html")
    public String footerNote(@RequestParam(value = "title", defaultValue = "") String title) {
        Map<String, String> parts = new HashMap<>();
        parts.put("title", title);
        parts.put("footer", "Prices include VAT. Delivery times are estimates.");
        parts.put("contact", "<a href=\"/contact\">Contact us</a>");
        return "<footer><small>" + parts.get("footer") + "</small> " + parts.get("contact") + "</footer>";
    }
}
