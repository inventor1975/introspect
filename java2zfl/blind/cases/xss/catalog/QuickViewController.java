package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QuickViewController {

    @GetMapping(value = "/catalog/quick-view", produces = MediaType.TEXT_HTML_VALUE)
    public String quickView(@RequestParam("title") String title,
                            @RequestParam(value = "price", defaultValue = "") String price) {
        String priceText = price.isEmpty() ? "Price on request" : "$" + price;
        return "<div class=\"quick-view\">" + ProductSnippets.card(title, priceText) + "</div>";
    }
}
