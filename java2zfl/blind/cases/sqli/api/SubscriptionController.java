package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SubscriptionController {

    private final JdbcTemplate jdbc;

    public SubscriptionController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/subscriptions")
    public List<Map<String, Object>> find(@RequestParam Map<String, String> filters) {
        StringBuilder sql = new StringBuilder("SELECT id, plan_code, status FROM subscriptions");
        String glue = " WHERE ";
        for (Map.Entry<String, String> f : filters.entrySet()) {
            if (f.getValue() == null || f.getValue().isEmpty()) {
                continue;
            }
            sql.append(glue).append(f.getKey()).append(" = '").append(f.getValue()).append("'");
            glue = " AND ";
        }
        return jdbc.queryForList(sql.toString());
    }
}
