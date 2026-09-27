package blind2.xss.spring;

import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AppearanceController {

    @GetMapping(value = "/shell", produces = "text/html")
    public String shell(@CookieValue(value = "accent", defaultValue = "#3366cc") String accent,
                        @CookieValue(value = "density", defaultValue = "normal") String density) {
        return "<!DOCTYPE html><html><head><style>:root{--accent:" + accent + ";}</style></head>"
                + "<body class=\"density-" + density + "\"><div id=\"app\"></div></body></html>";
    }
}
