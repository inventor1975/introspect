package blind.sqli.api;

import java.util.List;
import java.util.function.Function;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuditController {

    record AuditEntry(long id, String actor, String action, String at) {
    }

    private final JdbcTemplate jdbc;

    public AuditController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/audit")
    public List<AuditEntry> entries(@RequestParam(required = false) String actor) {
        Function<String, String> where = a -> a == null ? "" : " WHERE actor = '" + a + "'";
        String sql = "SELECT id, actor, action, created_at FROM audit_log" + where.apply(actor)
                + " ORDER BY created_at DESC LIMIT 200";
        return jdbc.query(sql, (rs, n) -> new AuditEntry(
                rs.getLong("id"), rs.getString("actor"), rs.getString("action"), rs.getString("created_at")));
    }
}
