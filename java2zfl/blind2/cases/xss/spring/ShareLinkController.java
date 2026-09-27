package blind2.xss.spring;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ShareLinkController {

    @GetMapping(value = "/share/buttons", produces = "text/html")
    public String buttons(@RequestParam("title") String title) {
        String encoded = URLEncoder.encode(title, StandardCharsets.UTF_8);
        return "<div class=\"share\">"
                + "<a href=\"https://social.example/share?text=" + encoded + "\">Share</a>"
                + "<a href=\"mailto:?subject=" + encoded + "\">E-mail</a>"
                + "</div>";
    }
}
