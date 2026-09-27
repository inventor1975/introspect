package blind.sqli.api;

import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CalendarViewController {

    private final JdbcTemplate jdbc;

    public CalendarViewController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/calendar")
    public ResponseEntity<List<Map<String, Object>>> view(@RequestParam(defaultValue = "week") String view,
                                                          @RequestParam String from) {
        LocalDate start;
        try {
            start = LocalDate.parse(from);
        } catch (DateTimeParseException e) {
            return ResponseEntity.badRequest().build();
        }
        LocalDate end = switch (view) {
            case "day" -> start.plusDays(1);
            case "month" -> start.plusMonths(1);
            default -> start.plusWeeks(1);
        };
        String sql = "SELECT id, title, starts_at, ends_at FROM calendar_events WHERE starts_at >= DATE '" + start
                + "' AND starts_at < DATE '" + end + "' ORDER BY starts_at";
        return ResponseEntity.ok(jdbc.queryForList(sql));
    }
}
