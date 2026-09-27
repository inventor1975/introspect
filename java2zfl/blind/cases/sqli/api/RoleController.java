package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RoleController {

    private final JdbcTemplate jdbc;

    public RoleController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/roles/members")
    public List<Map<String, Object>> members(@RequestParam List<String> roles) {
        String inList = roles.stream()
                .filter(r -> !r.isBlank())
                .map(String::toUpperCase)
                .collect(Collectors.joining("','", "'", "'"));
        return jdbc.queryForList("SELECT u.login, r.name FROM users u JOIN user_roles ur ON ur.user_id = u.id"
                + " JOIN roles r ON r.id = ur.role_id WHERE r.name IN (" + inList + ")");
    }
}
