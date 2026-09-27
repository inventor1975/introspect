package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReviewController {

    private final JdbcTemplate jdbc;

    public ReviewController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/products/{productId}/reviews")
    public List<Map<String, Object>> reviews(@PathVariable Long productId,
                                             @RequestParam(defaultValue = "0") Integer minStars) {
        String sql = "SELECT author, stars, body, created_at FROM reviews WHERE product_id = " + productId
                + " AND stars >= " + minStars + " ORDER BY created_at DESC";
        return jdbc.queryForList(sql);
    }
}
