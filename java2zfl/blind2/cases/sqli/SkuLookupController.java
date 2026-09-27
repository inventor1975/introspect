package blind2.sqli;

import java.util.Map;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SkuLookupController {

    private static final String BY_SKU = """
            SELECT sku, description, unit_price
              FROM catalog_items
             WHERE sku = '%s'
               AND discontinued = false
            """;

    private final JdbcTemplate jdbc;

    public SkuLookupController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/items/{sku}")
    public ResponseEntity<Map<String, Object>> item(@PathVariable String sku) {
        try {
            return ResponseEntity.ok(jdbc.queryForMap(BY_SKU.formatted(sku)));
        } catch (EmptyResultDataAccessException e) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
