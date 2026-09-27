package blind.sqli.api;

import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WebhookController {

    private final JdbcTemplate jdbc;

    public WebhookController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping(value = "/hooks/courier", consumes = "text/plain")
    public ResponseEntity<Void> receive(@RequestBody String payload) {
        String[] lines = payload.split("\\R");
        if (lines.length < 2) {
            return ResponseEntity.badRequest().build();
        }
        String event = lines[0].trim();
        String reference = lines[1].trim();
        jdbc.update("INSERT INTO courier_events (event, reference, received_at) VALUES ('" + event + "', ?, CURRENT_TIMESTAMP)",
                reference);
        return ResponseEntity.ok().build();
    }
}
