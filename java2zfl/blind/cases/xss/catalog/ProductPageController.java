package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class ProductPageController {

    @GetMapping(value = "/p/{slug}", produces = MediaType.TEXT_HTML_VALUE)
    @ResponseBody
    public String page(@PathVariable("slug") String slug) {
        String title = slug.replace('-', ' ');
        return "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>"
                + "<h1 class=\"product-title\">" + title + "</h1>"
                + "<div id=\"details\" data-src=\"/api/products/by-slug\"></div>"
                + "</body></html>";
    }
}
