package blind.xss.account;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProfileAwardPreviewController {

    @GetMapping(value = "/account/award/preview", produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@RequestParam("label") String label,
                          @RequestParam(value = "tier", defaultValue = "bronze") String tier) {
        AwardRenderer renderer = new TextAwardRenderer();
        String award = renderer.render(label, tier);
        return "<div class=\"award-preview\">" + award + "<p>Preview only &mdash; not saved.</p></div>";
    }
}
