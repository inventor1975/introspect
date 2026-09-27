package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportController {

    private final JdbcTemplate jdbc;

    public ReportController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/reports/sales")
    public List<Map<String, Object>> sales(@RequestParam List<String> columns) {
        String projection = columns.stream()
                .map(String::trim)
                .filter(c -> !c.isEmpty())
                .distinct()
                .collect(Collectors.joining(", "));
        if (projection.isEmpty()) {
            projection = "region, SUM(revenue)";
        }
        return jdbc.queryForList("SELECT " + projection + " FROM sales_fact GROUP BY region");
    }
}
