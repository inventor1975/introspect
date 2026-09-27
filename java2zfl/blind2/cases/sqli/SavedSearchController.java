package blind2.sqli;

import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SavedSearchController {

    private final JdbcTemplate jdbc;
    private volatile String currentQueue = "general";

    public SavedSearchController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/tickets/queue")
    public ResponseEntity<Void> switchQueue(@RequestParam String queue) {
        currentQueue = queue.trim();
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @GetMapping("/api/tickets/current")
    public List<Map<String, Object>> current() {
        return jdbc.queryForList("SELECT id, subject, priority FROM tickets WHERE queue = '" + currentQueue
                + "' AND closed_at IS NULL ORDER BY priority DESC");
    }
}
