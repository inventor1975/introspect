package blind.xss.account;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProfileAwardController {

    private final AwardRenderer awardRenderer;

    public ProfileAwardController(AwardRenderer awardRenderer) {
        this.awardRenderer = awardRenderer;
    }

    @GetMapping(value = "/account/award", produces = MediaType.TEXT_HTML_VALUE)
    public String award(@RequestParam("label") String label,
                        @RequestParam(value = "tier", defaultValue = "bronze") String tier) {
        return "<div class=\"award-preview\">" + awardRenderer.render(label, tier) + "</div>";
    }
}
