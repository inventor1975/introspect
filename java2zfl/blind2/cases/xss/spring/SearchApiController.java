package blind2.xss.spring;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchApiController {

    @GetMapping("/api/search")
    public Map<String, Object> search(@RequestParam("q") String q,
                                      @RequestParam(value = "limit", defaultValue = "10") int limit) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("query", q);
        result.put("echo", "<em>" + q + "</em>");
        result.put("limit", limit);
        result.put("items", List.of());
        return result;
    }
}
