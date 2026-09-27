package blind2.sqli;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProjectSearchController {

    private final NamedParameterJdbcTemplate named;

    public ProjectSearchController(NamedParameterJdbcTemplate named) {
        this.named = named;
    }

    @GetMapping("/api/projects")
    public List<String> projects(@RequestParam("owner") String owner,
                                 @RequestParam(value = "status", required = false) String status) {
        Map<String, Object> params = new HashMap<>();
        params.put("owner", owner);
        String sql = "SELECT name FROM projects WHERE owner_login = :owner";
        if (status != null && !status.isBlank()) {
            sql += " AND status = :status";
            params.put("status", status);
        }
        sql += " ORDER BY name";
        return named.query(sql, params, (rs, rowNum) -> rs.getString("name"));
    }
}
