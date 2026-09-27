package blind.xss.reports;

import java.util.List;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class ExportController {

    @GetMapping(value = "/reports/export/preview", produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@RequestParam("columns") List<String> columns,
                          @RequestParam(value = "title", defaultValue = "Export") String title) {
        StringBuilder html = new StringBuilder("<table class=\"export\"><caption>");
        html.append(HtmlUtils.htmlEscape(title)).append("</caption><thead><tr>");
        for (String column : columns) {
            html.append("<th>").append(column).append("</th>");
        }
        html.append("</tr></thead></table>");
        return html.toString();
    }
}
