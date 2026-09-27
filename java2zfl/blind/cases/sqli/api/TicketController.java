package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TicketController {

    private static final String OPEN_FOR_ASSIGNEE = """
            SELECT t.id, t.subject, t.priority
              FROM tickets t
             WHERE t.assignee = '%s'
               AND t.closed = FALSE
             ORDER BY t.priority DESC, t.opened_at
            """;

    private final JdbcTemplate jdbc;

    public TicketController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/agents/{login}/tickets")
    public List<Map<String, Object>> open(@PathVariable("login") String assignee) {
        return jdbc.queryForList(OPEN_FOR_ASSIGNEE.formatted(assignee));
    }
}
