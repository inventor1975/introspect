package blind.xss.catalog;

import java.util.Map;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StoreHoursController {

    private static final Map<Integer, String> HOURS = Map.of(
            1, "Mon-Sat 9:00-20:00, Sun 10:00-16:00",
            2, "Mon-Fri 10:00-18:00",
            3, "Daily 8:00-22:00");

    @GetMapping(value = "/stores/{storeId}/hours", produces = MediaType.TEXT_HTML_VALUE)
    public String hours(@PathVariable("storeId") int storeId) {
        String hours = HOURS.getOrDefault(storeId, "Opening hours not published yet");
        return "<p class=\"hours\">Store " + storeId + ": " + hours + "</p>";
    }
}
