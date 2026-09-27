package blind.xss.catalog;

import java.math.BigDecimal;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QuickPriceController {

    @GetMapping("/catalog/quick-price")
    public ResponseEntity<String> quickPrice(@RequestParam("title") String title,
                                             @RequestParam("price") String price) {
        BigDecimal amount;
        try {
            amount = new BigDecimal(price);
        } catch (NumberFormatException e) {
            return ResponseEntity.badRequest().contentType(MediaType.TEXT_HTML).body("<p>Invalid price.</p>");
        }
        String html = "<div class=\"quick-view\">" + ProductSnippets.safeCard(title, amount) + "</div>";
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(html);
    }
}
