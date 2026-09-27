package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ShipmentStatusController {

    private final JdbcTemplate jdbc;

    public ShipmentStatusController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/shipments/{id}/events")
    public ResponseEntity<List<Map<String, Object>>> events(@PathVariable String id) {
        UUID shipmentId;
        try {
            shipmentId = UUID.fromString(id);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(jdbc.queryForList(
                "SELECT status, location, occurred_at FROM shipment_events WHERE shipment_id = '"
                        + shipmentId + "' ORDER BY occurred_at"));
    }
}
