package blind.sqli.api;

import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FeatureFlagController {

    private final JdbcTemplate jdbc;

    @Value("${flags.table:feature_flags}")
    private String flagsTable;

    public FeatureFlagController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/flags/{name}")
    public Map<String, Object> flag(@PathVariable String name) {
        return jdbc.queryForMap("SELECT name, enabled, rollout_pct FROM " + flagsTable + " WHERE name = ?", name);
    }
}
