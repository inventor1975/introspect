package blind.sqli.api;

import java.util.Map;
import java.util.Optional;
import java.util.Set;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PromotionLookupController {

    private static final Set<String> CAMPAIGNS = Set.of("SPRING", "SUMMER", "BLACKFRIDAY", "HOLIDAY");

    private final JdbcTemplate jdbc;

    public PromotionLookupController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/promotions/current")
    public Map<String, Object> current(@RequestParam(required = false) String campaign) {
        String code = Optional.ofNullable(campaign)
                .map(String::trim)
                .map(String::toUpperCase)
                .map(c -> CAMPAIGNS.contains(c) ? c : "DEFAULT")
                .orElse("DEFAULT");
        return jdbc.queryForMap("SELECT code, discount_pct, ends_on FROM promotions WHERE campaign = '" + code
                + "' AND ends_on >= CURRENT_DATE");
    }
}
