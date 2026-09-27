package blind.xss.catalog;

import java.util.function.Function;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CouponController {

    @GetMapping(value = "/cart/coupon/expired", produces = MediaType.TEXT_HTML_VALUE)
    public String expired(@RequestParam("code") String code) {
        Function<String, String> highlight = c -> "<em class=\"coupon\">" + c.strip() + "</em>";
        return "<p class=\"notice\">The coupon " + highlight.apply(code) + " has expired.</p>";
    }
}
