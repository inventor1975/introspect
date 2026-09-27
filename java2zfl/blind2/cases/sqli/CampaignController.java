package blind2.sqli;

import java.util.List;
import java.util.Map;
import org.apache.commons.text.StringEscapeUtils;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CampaignController {

    private final JdbcTemplate jdbc;

    public CampaignController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/campaigns")
    public List<Map<String, Object>> byName(@RequestParam String name) {
        String cleaned = StringEscapeUtils.escapeHtml4(name.trim());
        return jdbc.queryForList("SELECT id, name, starts_on, ends_on FROM campaigns WHERE name = '" + cleaned + "'");
    }
}
