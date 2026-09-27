package blind.sqli.api;

import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LoyaltyController {

    private final JdbcTemplate jdbc;

    public LoyaltyController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/loyalty/points")
    public Map<String, Object> points(@RequestParam String cardNumber) {
        String escaped = cardNumber.replace("'", "\\'");
        return jdbc.queryForMap("SELECT holder, points, tier FROM loyalty_cards WHERE card_number = '" + escaped + "'");
    }
}
