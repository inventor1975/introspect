package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProjectController {

    private final JdbcTemplate jdbc;

    public ProjectController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/projects")
    public List<Map<String, Object>> projects(@RequestParam(required = false) String owner,
                                              @RequestParam(defaultValue = "false") boolean includeArchived) {
        StringBuilder sql = new StringBuilder("SELECT id, name, owner, updated_at FROM projects WHERE 1 = 1");
        if (!includeArchived) {
            sql.append(" AND archived = FALSE");
        }
        appendOwnerFilter(sql, owner);
        sql.append(" ORDER BY updated_at DESC");
        return jdbc.queryForList(sql.toString());
    }

    private static void appendOwnerFilter(StringBuilder sql, String owner) {
        if (owner == null || owner.isEmpty()) {
            return;
        }
        sql.append(" AND owner = '").append(owner).append('\'');
    }
}
