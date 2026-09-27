package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/catalog")
public class ProductSearchController {

    @GetMapping(value = "/search", produces = MediaType.TEXT_HTML_VALUE)
    public String search(@RequestParam("q") String query,
                         @RequestParam(value = "page", defaultValue = "1") int page) {
        return "<div class=\"results\">"
                + "<h2>Search results for " + query + "</h2>"
                + "<p class=\"pager\">Page " + page + "</p>"
                + "</div>";
    }
}
