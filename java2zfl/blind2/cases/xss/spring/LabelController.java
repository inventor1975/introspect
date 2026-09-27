package blind2.xss.spring;

import java.util.function.Function;
import org.owasp.encoder.Encode;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LabelController {

    private static final Function<String, String> DISPLAY =
            ((Function<String, String>) String::trim).andThen(Encode::forHtml);

    @GetMapping("/labels/print")
    public String print(@RequestParam("line1") String line1,
                        @RequestParam(value = "line2", defaultValue = "") String line2) {
        return "<div class=\"label\"><div>" + DISPLAY.apply(line1) + "</div><div>"
                + DISPLAY.apply(line2) + "</div></div>";
    }
}
