package blind2.sqli;

import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RecentOrdersController {

    public record OrderRow(long id, String reference, String status) {
    }

    private final JdbcTemplate jdbc;

    public RecentOrdersController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/orders/recent")
    public List<OrderRow> recent(@RequestParam(value = "contains", required = false) String contains) {
        List<OrderRow> rows = jdbc.query(
                "SELECT id, reference, status FROM orders WHERE created_at > now() - interval '1 day' ORDER BY created_at DESC",
                (rs, rowNum) -> new OrderRow(rs.getLong(1), rs.getString(2), rs.getString(3)));
        if (contains == null || contains.isBlank()) {
            return rows;
        }
        String needle = contains.trim().toLowerCase(Locale.ROOT);
        return rows.stream()
                .filter(r -> r.reference() != null && r.reference().toLowerCase(Locale.ROOT).contains(needle))
                .collect(Collectors.toList());
    }
}
