package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StatsController {

    private static final Map<String, String> METRIC_COLUMNS = Map.of(
            "views", "page_views",
            "visitors", "unique_visitors",
            "bounce", "bounce_rate");

    private final JdbcTemplate jdbc;

    public StatsController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/stats/daily")
    public List<Map<String, Object>> daily(@RequestParam String metric) {
        String column = METRIC_COLUMNS.getOrDefault(metric, metric);
        return jdbc.queryForList("SELECT day, " + column + " AS value FROM daily_stats ORDER BY day DESC LIMIT 30");
    }
}
