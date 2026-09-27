package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class ProductLookupController {

    @GetMapping(value = "/catalog/lookup", produces = MediaType.TEXT_HTML_VALUE)
    public String lookup(@RequestParam("id") long id,
                         @RequestParam(value = "ref", required = false) String partnerRef) {
        String via = partnerRef == null ? "" : "<p class=\"via\">Referred by " + HtmlUtils.htmlEscape(partnerRef) + "</p>";
        return "<h2>Product #" + id + "</h2>" + via + "<div id=\"product\" data-id=\"" + id + "\"></div>";
    }
}
