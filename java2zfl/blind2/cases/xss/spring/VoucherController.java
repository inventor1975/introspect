package blind2.xss.spring;

import java.util.Optional;
import org.owasp.encoder.Encode;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VoucherController {

    @GetMapping("/gift/voucher")
    public String voucher(@RequestParam(value = "for", required = false) String recipient,
                          @RequestParam(value = "msg", required = false) String message) {
        String who = Optional.ofNullable(recipient).map(String::trim).map(Encode::forHtml).orElse("you");
        String note = Optional.ofNullable(message).map(Encode::forHtml).orElse("");
        return "<div class=\"voucher\"><h2>A gift for " + who + "</h2><p>" + note + "</p></div>";
    }
}
