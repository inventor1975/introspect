package blind.xss.catalog;

import org.jsoup.Jsoup;
import org.jsoup.safety.Safelist;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReviewController {

    @PostMapping(value = "/catalog/reviews/preview", produces = MediaType.TEXT_HTML_VALUE)
    public String preview(@RequestParam("body") String body, @RequestParam("rating") int rating) {
        int stars = Math.max(1, Math.min(5, rating));
        String cleaned = Jsoup.clean(body, Safelist.basic());
        return "<div class=\"review\" data-rating=\"" + stars + "\">"
                + "<div class=\"stars\">" + "&#9733;".repeat(stars) + "</div>"
                + "<div class=\"review-body\">" + cleaned + "</div>"
                + "</div>";
    }
}
