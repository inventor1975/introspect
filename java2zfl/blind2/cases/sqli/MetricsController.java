package blind2.sqli;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MetricsController {

    private final NamedParameterJdbcTemplate named;

    public MetricsController(NamedParameterJdbcTemplate named) {
        this.named = named;
    }

    @GetMapping("/api/metrics/{name}")
    public List<Map<String, Object>> series(@PathVariable("name") String metric,
                                            @RequestParam("from") String from) {
        Map<String, Object> params = Map.of("from", from);
        return named.queryForList(
                "SELECT ts, value FROM metrics_" + metric + " WHERE ts >= CAST(:from AS timestamp) ORDER BY ts",
                params);
    }
}
