package blind2.sqli;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RecentlyViewedController {

    private final JdbcTemplate jdbc;

    public RecentlyViewedController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/recently-viewed/count")
    public int count(@CookieValue(value = "visitor", defaultValue = "") String visitorId) {
        if (visitorId.isEmpty()) {
            return 0;
        }
        Integer n = jdbc.queryForObject(
                "SELECT count(DISTINCT product_id) FROM product_views WHERE visitor_id = '" + visitorId + "'"
                        + " AND viewed_at > now() - interval '7 days'",
                Integer.class);
        return n == null ? 0 : n;
    }
}
