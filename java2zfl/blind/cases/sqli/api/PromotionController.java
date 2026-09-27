package blind.sqli.api;

import java.util.Map;
import java.util.Optional;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PromotionController {

    private final JdbcTemplate jdbc;

    public PromotionController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/promotions/current")
    public Map<String, Object> current(@RequestParam(required = false) String campaign) {
        String code = Optional.ofNullable(campaign)
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .orElse("DEFAULT");
        return jdbc.queryForMap("SELECT code, discount_pct, ends_on FROM promotions WHERE campaign = '" + code
                + "' AND ends_on >= CURRENT_DATE");
    }
}
