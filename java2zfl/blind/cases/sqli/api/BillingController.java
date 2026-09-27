package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BillingController {

    private static final Map<String, String> SAVED_FILTERS = new ConcurrentHashMap<>();

    private final JdbcTemplate jdbc;

    public BillingController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @PostMapping("/api/billing/filter")
    public ResponseEntity<Void> saveFilter(@RequestHeader("X-User") String user,
                                           @RequestParam String planCode) {
        SAVED_FILTERS.put(user, planCode);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/api/billing/subscriptions")
    public List<Map<String, Object>> subscriptions(@RequestHeader("X-User") String user) {
        String plan = SAVED_FILTERS.getOrDefault(user, "BASIC");
        return jdbc.queryForList("SELECT id, customer_id, renews_on FROM subscriptions WHERE plan_code = '"
                + plan + "' ORDER BY renews_on");
    }
}
