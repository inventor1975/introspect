package blind2.sqli;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BulkArchiveController {

    private final JdbcTemplate jdbc;

    public BulkArchiveController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/messages/archive")
    public ResponseEntity<Integer> archive(@RequestParam("ids") List<Long> ids) {
        if (ids.isEmpty()) {
            return ResponseEntity.ok(0);
        }
        String in = ids.stream().map(String::valueOf).collect(Collectors.joining(","));
        int n = jdbc.update("UPDATE messages SET archived = true, archived_at = now() WHERE id IN (" + in + ")");
        return ResponseEntity.ok(n);
    }
}
