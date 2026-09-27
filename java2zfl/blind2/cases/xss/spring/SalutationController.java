package blind2.xss.spring;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
@RequestMapping("/cards")
public class SalutationController {

    @GetMapping(value = "/salutation", produces = "text/html")
    public String salutation(@RequestParam("to") String to,
                             @RequestParam(value = "from", required = false) String from) {
        StringBuilder html = new StringBuilder("<div class=\"card\">");
        html.append("<p>Dear ").append(HtmlUtils.htmlEscape(to)).append(",</p>");
        html.append("<p>Happy holidays!</p>");
        if (from != null) {
            html.append("<p class=\"sig\">").append(HtmlUtils.htmlEscape(from)).append("</p>");
        }
        return html.append("</div>").toString();
    }
}
