package blind.xss.reports;

import java.util.Map;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DashboardController {

    @GetMapping(value = "/reports/dashboard/filters", produces = MediaType.TEXT_HTML_VALUE)
    public String filters(@RequestParam Map<String, String> filters) {
        StringBuilder chips = new StringBuilder();
        filters.forEach((key, value) -> chips.append("<span class=\"chip\">")
                .append(key).append(": ").append(value)
                .append("</span>"));
        return "<section class=\"active-filters\">" + chips + "</section>";
    }
}
