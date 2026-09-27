package blind2.sqli;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BulkPriceController {

    public record PriceChange(String sku, BigDecimal price) {
    }

    private final JdbcTemplate jdbc;

    public BulkPriceController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/prices/bulk")
    public int[] apply(@RequestBody List<PriceChange> changes) {
        String[] statements = changes.stream()
                .filter(c -> c.price() != null && c.price().signum() > 0)
                .map(c -> "UPDATE prices SET amount = " + c.price().toPlainString() + ", updated_at = now() WHERE sku = '"
                        + c.sku() + "'")
                .toArray(String[]::new);
        return jdbc.batchUpdate(statements);
    }
}
