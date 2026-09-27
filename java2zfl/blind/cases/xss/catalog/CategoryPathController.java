package blind.xss.catalog;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CategoryPathController {

    private static final Pattern SEGMENT = Pattern.compile("[a-z0-9-]{1,40}");

    @GetMapping(value = "/catalog/breadcrumbs", produces = MediaType.TEXT_HTML_VALUE)
    public String breadcrumbs(@RequestParam("path") String path) {
        List<String> clean = new ArrayList<>();
        for (String segment : path.toLowerCase().split("/")) {
            if (!SEGMENT.matcher(segment).matches()) {
                continue;
            }
            clean.add(segment);
        }
        StringBuilder html = new StringBuilder("<ol class=\"breadcrumbs\"><li><a href=\"/catalog\">Catalog</a></li>");
        String prefix = "/catalog";
        for (String segment : clean) {
            prefix = prefix + "/" + segment;
            html.append("<li><a href=\"").append(prefix).append("\">").append(segment).append("</a></li>");
        }
        return html.append("</ol>").toString();
    }
}
