package blind.xss.catalog;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.util.HtmlUtils;

@Controller
public class ProductSlugController {

    @GetMapping(value = "/p/{slug}/specs", produces = MediaType.TEXT_HTML_VALUE)
    @ResponseBody
    public String specs(@PathVariable("slug") String slug) {
        String title = HtmlUtils.htmlEscape(slug.replace('-', ' '));
        return "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>"
                + "<h1 class=\"product-title\">" + title + " &ndash; specifications</h1>"
                + "<table id=\"specs\"></table>"
                + "</body></html>";
    }
}
