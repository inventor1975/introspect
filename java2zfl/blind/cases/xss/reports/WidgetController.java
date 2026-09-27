package blind.xss.reports;

import java.util.Map;
import java.util.Set;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class WidgetController {

    private static final Set<String> KNOWN_FILTERS = Set.of("region", "segment", "channel");

    @GetMapping(value = "/reports/widget/filters", produces = MediaType.TEXT_HTML_VALUE)
    public String filters(@RequestParam Map<String, String> params) {
        StringBuilder html = new StringBuilder("<ul class=\"widget-filters\">");
        for (Map.Entry<String, String> entry : params.entrySet()) {
            if (!KNOWN_FILTERS.contains(entry.getKey())) {
                continue;
            }
            html.append("<li>").append(entry.getKey()).append(" = ")
                    .append(HtmlUtils.htmlEscape(entry.getValue())).append("</li>");
        }
        return html.append("</ul>").toString();
    }
}
