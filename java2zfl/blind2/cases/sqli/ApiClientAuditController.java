package blind2.sqli;

import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ApiClientAuditController {

    private final JdbcTemplate jdbc;

    public ApiClientAuditController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/ping")
    public Map<String, Object> ping(@RequestHeader(value = "X-Client-Id", defaultValue = "anonymous") String clientId) {
        jdbc.execute("INSERT INTO api_calls(client_id, endpoint, called_at) VALUES ('" + clientId + "', '/api/ping', now())");
        return Map.of("status", "ok");
    }
}
