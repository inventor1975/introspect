package blind.xss.catalog;

import java.util.function.Function;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

@RestController
public class CouponCheckController {

    @GetMapping(value = "/cart/coupon/check", produces = MediaType.TEXT_HTML_VALUE)
    public String check(@RequestParam("code") String code) {
        Function<String, String> highlight = c -> "<em class=\"coupon\">" + HtmlUtils.htmlEscape(c.strip()) + "</em>";
        return "<p class=\"notice\">Checking coupon " + highlight.apply(code) + "&hellip;</p>";
    }
}
