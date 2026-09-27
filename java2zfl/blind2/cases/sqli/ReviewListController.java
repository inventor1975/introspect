package blind2.sqli;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReviewListController {

    enum Direction { ASC, DESC }

    private final JdbcTemplate jdbc;

    public ReviewListController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/products/{productId}/reviews")
    public List<Map<String, Object>> reviews(@PathVariable long productId,
                                             @RequestParam(value = "order", defaultValue = "desc") String order) {
        Direction direction;
        try {
            direction = Direction.valueOf(order.trim().toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            direction = Direction.DESC;
        }
        return jdbc.queryForList("SELECT id, rating, created_at FROM reviews WHERE product_id = " + productId
                + " AND approved = true ORDER BY created_at " + direction.name() + " LIMIT 50");
    }
}
