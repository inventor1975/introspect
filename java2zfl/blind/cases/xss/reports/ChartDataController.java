package blind.xss.reports;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class ChartDataController {

    @GetMapping("/reports/chart/embed")
    public ResponseEntity<String> embed(@RequestParam("series") String seriesId,
                                        @RequestParam(value = "label", defaultValue = "Revenue") String label) {
        if (seriesId.isEmpty() || seriesId.length() > 12 || !seriesId.chars().allMatch(Character::isDigit)) {
            return ResponseEntity.badRequest().contentType(MediaType.TEXT_PLAIN).body("invalid series id");
        }
        String html = "<figure class=\"chart\">"
                + "<figcaption>" + HtmlUtils.htmlEscape(label) + "</figcaption>"
                + "<div id=\"chart\"></div>"
                + "<script>Charts.render('chart', " + seriesId + ");</script>"
                + "</figure>";
        return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(html);
    }
}
