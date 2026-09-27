package blind.sqli.api;

import java.util.ArrayList;
import java.util.List;
import java.util.function.BiFunction;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuditEventController {

    record AuditEntry(long id, String actor, String action) {
    }

    private final JdbcTemplate jdbc;

    public AuditEventController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/audit")
    public List<AuditEntry> entries(@RequestParam(required = false) String actor,
                                    @RequestParam(required = false) String action) {
        List<Object> args = new ArrayList<>();
        BiFunction<String, String, String> cond = (column, value) -> {
            if (value == null) {
                return "";
            }
            args.add(value);
            return " AND " + column + " = ?";
        };
        String sql = "SELECT id, actor, action FROM audit_log WHERE 1 = 1"
                + cond.apply("actor", actor)
                + cond.apply("action", action)
                + " ORDER BY created_at DESC LIMIT 200";
        return jdbc.query(sql, (rs, n) -> new AuditEntry(rs.getLong(1), rs.getString(2), rs.getString(3)), args.toArray());
    }
}
