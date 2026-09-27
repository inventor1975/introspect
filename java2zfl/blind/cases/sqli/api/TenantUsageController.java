package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TenantUsageController {

    private static final Map<String, String> TENANT_SCHEMAS = Map.of(
            "acme", "t_acme",
            "globex", "t_globex",
            "initech", "t_initech");

    private final NamedParameterJdbcTemplate named;

    public TenantUsageController(NamedParameterJdbcTemplate named) {
        this.named = named;
    }

    @GetMapping("/api/usage/monthly")
    public ResponseEntity<List<Map<String, Object>>> monthly(@RequestHeader("X-Tenant") String tenant,
                                                             @RequestParam int year) {
        String schema = TENANT_SCHEMAS.get(tenant.toLowerCase());
        if (schema == null) {
            return ResponseEntity.badRequest().build();
        }
        String sql = "SELECT month, api_calls, storage_gb FROM " + schema + ".usage WHERE year = :year ORDER BY month";
        return ResponseEntity.ok(named.queryForList(sql, Map.of("year", year)));
    }
}
