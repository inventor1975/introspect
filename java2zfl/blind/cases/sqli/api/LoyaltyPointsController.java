package blind.sqli.api;

import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LoyaltyPointsController {

    private final JdbcTemplate jdbc;

    public LoyaltyPointsController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/loyalty/points")
    public ResponseEntity<Map<String, Object>> points(@RequestParam String cardNumber) {
        String card = cardNumber.strip();
        if (card.isEmpty() || card.length() > 19 || !card.chars().allMatch(ch -> ch >= '0' && ch <= '9')) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(jdbc.queryForMap(
                "SELECT holder, points, tier FROM loyalty_cards WHERE card_number = '" + card + "'"));
    }
}
