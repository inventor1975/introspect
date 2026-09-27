package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SalesReportController {

    private static final Set<String> ALLOWED_COLUMNS = Set.of("region", "product_line", "channel", "quarter");

    private final JdbcTemplate jdbc;

    public SalesReportController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/reports/sales")
    public List<Map<String, Object>> sales(@RequestParam List<String> groupBy) {
        String dims = groupBy.stream()
                .map(String::trim)
                .map(String::toLowerCase)
                .filter(ALLOWED_COLUMNS::contains)
                .distinct()
                .collect(Collectors.joining(", "));
        if (dims.isEmpty()) {
            dims = "region";
        }
        return jdbc.queryForList("SELECT " + dims + ", SUM(revenue) AS revenue FROM sales_fact GROUP BY " + dims);
    }
}
