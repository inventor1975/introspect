package blind2.xss.spring;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FooterController {

    @Value("${site.footer.html}")
    private String footerHtml;

    @Value("${site.support.email}")
    private String supportEmail;

    @GetMapping("/fragments/footer")
    public String footer(@RequestParam(value = "year", defaultValue = "2026") int year) {
        return "<footer>" + footerHtml + "<p>&copy; " + year + " &middot; <a href=\"mailto:"
                + supportEmail + "\">Support</a></p></footer>";
    }
}
