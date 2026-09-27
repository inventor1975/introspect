package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TenantReportController {

    private final NamedParameterJdbcTemplate named;

    public TenantReportController(NamedParameterJdbcTemplate named) {
        this.named = named;
    }

    @GetMapping("/api/reports/annual")
    public List<Map<String, Object>> annual(@RequestHeader("X-Tenant") String tenant,
                                            @RequestParam int year) {
        String sql = "SELECT month, revenue, cost FROM " + tenant + "_reports WHERE year = :year ORDER BY month";
        return named.queryForList(sql, Map.of("year", year));
    }
}
