package blind2.xss.spring;

import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FilterSummaryController {

    @GetMapping(value = "/listings/filters", produces = "text/html")
    public String filters(@RequestParam Map<String, String> params) {
        String chips = params.entrySet().stream()
                .filter(e -> !e.getKey().equals("page"))
                .map(e -> "<span class=\"chip\">" + e.getKey() + ": " + e.getValue() + "</span>")
                .collect(Collectors.joining(""));
        return "<div class=\"active-filters\">" + chips + "</div>";
    }
}
