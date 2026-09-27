package blind2.xss.spring;

import java.util.ArrayList;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportHeaderController {

    @GetMapping(value = "/reports/header", produces = "text/html")
    public String header(@RequestParam(value = "subtitle", defaultValue = "") String subtitle) {
        List<String> lines = new ArrayList<>();
        lines.add("<h1>Quarterly report</h1>");
        lines.add("<p class=\"meta\">Generated automatically</p>");
        lines.add(subtitle);
        StringBuilder html = new StringBuilder("<header>");
        for (int i = 0; i < 2; i++) {
            html.append(lines.get(i));
        }
        return html.append("</header>").toString();
    }
}
