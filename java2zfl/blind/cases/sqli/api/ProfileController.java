package blind.sqli.api;

import blind.sqli.support.RequestContext;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProfileController {

    private final JdbcTemplate jdbc;

    public ProfileController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/me")
    public Map<String, Object> me() {
        String user = RequestContext.userName();
        return jdbc.queryForMap("SELECT login, display_name, email, locale FROM users WHERE login = '" + user + "'");
    }
}
