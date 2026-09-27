package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TicketQueueController {

    private static final String OPEN_FOR_ASSIGNEE = """
            SELECT t.id, t.subject, t.priority
              FROM %s t
             WHERE t.assignee = ?
               AND t.priority >= ?
               AND t.closed = FALSE
             ORDER BY t.priority DESC, t.opened_at
            """;

    private final JdbcTemplate jdbc;

    public TicketQueueController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/agents/{login}/tickets")
    public List<Map<String, Object>> open(@PathVariable("login") String assignee,
                                          @RequestParam(defaultValue = "false") boolean escalated,
                                          @RequestParam(defaultValue = "1") int minPriority) {
        String table = escalated ? "escalated_tickets" : "tickets";
        return jdbc.queryForList(OPEN_FOR_ASSIGNEE.formatted(table), assignee, minPriority);
    }
}
