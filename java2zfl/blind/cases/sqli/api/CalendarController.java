package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CalendarController {

    private final JdbcTemplate jdbc;

    public CalendarController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/calendar")
    public List<Map<String, Object>> view(@RequestParam(defaultValue = "week") String view,
                                          @RequestParam String from) {
        String range = switch (view) {
            case "day" -> "starts_at >= DATE '" + from + "' AND starts_at < DATE '" + from + "' + 1";
            case "month" -> "starts_at >= DATE '" + from + "' AND starts_at < DATE '" + from + "' + INTERVAL '1 month'";
            default -> "starts_at >= DATE '" + from + "' AND starts_at < DATE '" + from + "' + 7";
        };
        return jdbc.queryForList("SELECT id, title, starts_at, ends_at FROM calendar_events WHERE " + range
                + " ORDER BY starts_at");
    }
}
