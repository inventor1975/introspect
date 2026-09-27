package blind.xss.account;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class ProfileAwardLegacyController {

    @GetMapping(value = "/legacy/award", produces = "text/html")
    @ResponseBody
    public String legacyAward(@RequestParam("label") String label) {
        AwardRenderer renderer = new HtmlAwardRenderer();
        return "<div class=\"legacy\">" + renderer.render(label, "legacy") + "</div>";
    }
}
