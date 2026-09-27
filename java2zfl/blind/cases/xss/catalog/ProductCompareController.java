package blind.xss.catalog;

import java.util.List;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProductCompareController {

    @GetMapping(value = "/catalog/compare", produces = MediaType.TEXT_HTML_VALUE)
    public String compare(@RequestParam("sku") List<String> skus) {
        List<String> cells = skus.stream()
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .distinct()
                .limit(4)
                .map(s -> "<th class=\"sku\">" + s + "</th>")
                .toList();
        return "<table class=\"compare\"><thead><tr>" + String.join("", cells) + "</tr></thead>"
                + "<tbody id=\"rows\"></tbody></table>";
    }
}
