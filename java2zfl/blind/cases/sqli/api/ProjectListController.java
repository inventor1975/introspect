package blind.sqli.api;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProjectListController {

    private final JdbcTemplate jdbc;

    public ProjectListController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/projects")
    public List<Map<String, Object>> projects(@RequestParam(required = false) String owner,
                                              @RequestParam(required = false) String team,
                                              @RequestParam(defaultValue = "false") boolean includeArchived) {
        StringBuilder sql = new StringBuilder("SELECT id, name, owner, updated_at FROM projects WHERE 1 = 1");
        List<Object> args = new ArrayList<>();
        if (!includeArchived) {
            sql.append(" AND archived = FALSE");
        }
        appendFilter(sql, args, "owner", owner);
        appendFilter(sql, args, "team_slug", team);
        sql.append(" ORDER BY updated_at DESC");
        return jdbc.queryForList(sql.toString(), args.toArray());
    }

    private static void appendFilter(StringBuilder sql, List<Object> args, String column, String value) {
        if (value == null || value.isEmpty()) {
            return;
        }
        sql.append(" AND ").append(column).append(" = ?");
        args.add(value);
    }
}
