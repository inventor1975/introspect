package blind.sqli.api;

import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WebhookReceiverController {

    private final JdbcTemplate jdbc;

    public WebhookReceiverController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping(value = "/hooks/payments", consumes = "text/plain")
    public ResponseEntity<Void> receive(@RequestBody String payload) {
        String[] lines = payload.split("\\R");
        if (lines.length < 2) {
            return ResponseEntity.badRequest().build();
        }
        EventType type;
        try {
            type = EventType.valueOf(lines[0].trim());
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
        String reference = lines[1].trim();
        jdbc.update("INSERT INTO payment_events (event, reference, received_at) VALUES ('" + type.name()
                + "', ?, CURRENT_TIMESTAMP)", reference);
        return ResponseEntity.ok().build();
    }
}
