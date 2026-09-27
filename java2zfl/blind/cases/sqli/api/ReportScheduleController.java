package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportScheduleController {

    private final JdbcTemplate jdbc;

    public ReportScheduleController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/reports/schedules")
    public List<Map<String, Object>> schedules(@RequestParam String owner) {
        String schema = System.getProperty("reports.schema", "reporting");
        return jdbc.queryForList("SELECT id, report_name, cron, next_run FROM " + schema
                + ".schedules WHERE owner = ? ORDER BY next_run", owner);
    }
}
