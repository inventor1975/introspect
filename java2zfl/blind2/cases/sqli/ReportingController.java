package blind2.sqli;

import java.sql.Date;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportingController {

    private final JdbcTemplate jdbc;

    @Value("${reporting.schema}")
    private String schema;

    public ReportingController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/kpis/daily")
    public List<Map<String, Object>> daily(@RequestParam("day") String day) {
        LocalDate date = LocalDate.parse(day);
        return jdbc.queryForList("SELECT kpi, value FROM " + schema + ".daily_kpis WHERE day = ? ORDER BY kpi",
                Date.valueOf(date));
    }
}
