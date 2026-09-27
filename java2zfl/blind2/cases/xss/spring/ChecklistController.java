package blind2.xss.spring;

import java.util.List;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class ChecklistController {

    @PostMapping(value = "/checklists/preview", produces = "text/html")
    public String preview(@RequestParam("title") String title,
                          @RequestParam("item") List<String> items) {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("<h3>%s (%d items)</h3><ul>", HtmlUtils.htmlEscape(title), items.size()));
        for (String item : items) {
            sb.append(String.format("<li><input type=\"checkbox\"> %s</li>", item));
        }
        return sb.append("</ul>").toString();
    }
}
