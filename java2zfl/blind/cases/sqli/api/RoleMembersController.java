package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RoleMembersController {

    private final JdbcTemplate jdbc;

    public RoleMembersController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/roles/members")
    public ResponseEntity<List<Map<String, Object>>> members(@RequestParam List<String> roleIds) {
        String inList;
        try {
            inList = roleIds.stream()
                    .filter(r -> !r.isBlank())
                    .map(String::trim)
                    .map(Long::parseLong)
                    .map(String::valueOf)
                    .collect(Collectors.joining(","));
        } catch (NumberFormatException e) {
            return ResponseEntity.badRequest().build();
        }
        if (inList.isEmpty()) {
            return ResponseEntity.ok(List.of());
        }
        return ResponseEntity.ok(jdbc.queryForList("SELECT u.login, ur.role_id FROM users u"
                + " JOIN user_roles ur ON ur.user_id = u.id WHERE ur.role_id IN (" + inList + ")"));
    }
}
