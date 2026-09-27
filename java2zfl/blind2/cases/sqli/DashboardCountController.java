package blind2.sqli;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DashboardCountController {

    private final JdbcTemplate jdbc;

    public DashboardCountController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/dashboard/accounts/count")
    public long count(@RequestParam("by") String by, @RequestParam("value") String value) {
        if ("country".equals(by)) {
            return countBy("country_code", value);
        }
        if ("plan".equals(by)) {
            return countBy("plan_code", value);
        }
        return countBy("status", value);
    }

    private long countBy(String column, String value) {
        Long n = jdbc.queryForObject("SELECT count(*) FROM accounts WHERE " + column + " = ?", Long.class, value);
        return n == null ? 0L : n;
    }
}
