package blind.xss.reports;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class ChartController {

    @GetMapping(value = "/reports/chart", produces = MediaType.TEXT_HTML_VALUE)
    public String chart(@RequestParam("series") String seriesId,
                        @RequestParam(value = "label", defaultValue = "Revenue") String label) {
        return "<figure class=\"chart\">"
                + "<figcaption>" + HtmlUtils.htmlEscape(label) + "</figcaption>"
                + "<div id=\"chart\"></div>"
                + "<script>Charts.render('chart', " + HtmlUtils.htmlEscape(seriesId) + ");</script>"
                + "</figure>";
    }
}
