package blind.sqli.api;

import java.util.Map;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrderDetailController {

    private final JdbcTemplate jdbc;

    public OrderDetailController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/orders/{orderId}")
    public ResponseEntity<Map<String, Object>> get(@PathVariable long orderId) {
        try {
            Map<String, Object> row = jdbc.queryForMap(
                    "SELECT id, status, total, placed_at FROM orders WHERE id = " + orderId);
            return ResponseEntity.ok(row);
        } catch (EmptyResultDataAccessException e) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
