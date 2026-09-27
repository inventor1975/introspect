package blind2.xss.spring;

import java.util.Map;
import blind2.xss.support.PlaceholderTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EventPageController {

    private static final PlaceholderTemplate PAGE = new PlaceholderTemplate(
            "<html><body><h1>{{event}}</h1><p>Hosted by {{host}}</p><a href=\"/rsvp\">RSVP</a></body></html>");

    @GetMapping(value = "/events/landing", produces = "text/html")
    public String landing(@RequestParam("event") String event,
                          @RequestParam(value = "host", defaultValue = "the organisers") String host) {
        return PAGE.fill(Map.of("event", event, "host", host));
    }
}
