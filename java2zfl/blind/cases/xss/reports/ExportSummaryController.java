package blind.xss.reports;

import java.util.List;
import java.util.Locale;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ExportSummaryController {

    enum ReportColumn {
        ORDER_ID("Order ID"), CUSTOMER("Customer"), TOTAL("Total"), CREATED("Created on");

        final String label;

        ReportColumn(String label) {
            this.label = label;
        }
    }

    @GetMapping(value = "/reports/export/summary", produces = MediaType.TEXT_HTML_VALUE)
    public String summary(@RequestParam("columns") List<String> columns) {
        StringBuilder html = new StringBuilder("<table class=\"export\"><thead><tr>");
        int ignored = 0;
        for (String requested : columns) {
            ReportColumn column;
            try {
                column = ReportColumn.valueOf(requested.trim().toUpperCase(Locale.ROOT));
            } catch (IllegalArgumentException e) {
                ignored++;
                continue;
            }
            html.append("<th>").append(column.label).append("</th>");
        }
        html.append("</tr></thead></table>");
        if (ignored > 0) {
            html.append("<p class=\"hint\">").append(ignored).append(" unknown column(s) were skipped.</p>");
        }
        return html.toString();
    }
}
