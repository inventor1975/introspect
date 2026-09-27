package blind2.xss.spring;

import java.util.HashMap;
import java.util.Map;
import blind2.xss.support.EscapingTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VenuePageController {

    private static final EscapingTemplate CARD = new EscapingTemplate(
            "<div class=\"venue\"><h2>{{name}}</h2><address>{{address}}</address></div>");

    @GetMapping(value = "/venues/card", produces = "text/html")
    public String card(@RequestParam("name") String name,
                       @RequestParam(value = "address", required = false) String address) {
        Map<String, String> values = new HashMap<>();
        values.put("name", name);
        values.put("address", address);
        return CARD.fill(values);
    }
}
