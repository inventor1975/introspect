package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ShipmentController {

    private final JdbcTemplate jdbc;

    public ShipmentController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/shipments/{id}/events")
    public List<Map<String, Object>> events(@PathVariable String id) {
        try {
            UUID.fromString(id);
        } catch (IllegalArgumentException e) {
            System.err.println("non-uuid shipment id supplied: " + id);
        }
        return jdbc.queryForList("SELECT status, location, occurred_at FROM shipment_events WHERE shipment_id = '"
                + id + "' ORDER BY occurred_at");
    }
}
