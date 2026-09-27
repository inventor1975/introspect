package blind.xss.reports;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportTitleController {

    @Value("${reports.default-title}")
    private String defaultTitle;

    @GetMapping(value = "/reports/annual", produces = MediaType.TEXT_HTML_VALUE)
    public String annual(@RequestParam(value = "year", defaultValue = "2025") int year) {
        return "<header class=\"report-header\"><h1>" + defaultTitle + "</h1>"
                + "<p class=\"period\">Fiscal year " + year + "</p></header>";
    }
}
