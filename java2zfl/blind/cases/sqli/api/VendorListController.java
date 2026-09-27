package blind.sqli.api;

import java.util.List;
import java.util.Map;
import java.util.Set;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VendorListController {

    private static final Set<String> STATUSES = Set.of("ACTIVE", "ONBOARDING", "SUSPENDED");
    private static final Set<String> REGIONS = Set.of("EU", "NA", "APAC", "LATAM");

    private final JdbcTemplate jdbc;

    public VendorListController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/vendors")
    public ResponseEntity<List<Map<String, Object>>> list(@RequestParam String status,
                                                          @RequestParam(defaultValue = "EU") String region) {
        if (!STATUSES.contains(status) || !REGIONS.contains(region)) {
            return ResponseEntity.badRequest().build();
        }
        List<Map<String, Object>> rows = jdbc.queryForList(
                "SELECT id, name, contact_email FROM vendors WHERE status = '" + status + "' AND region = '" + region + "'");
        return ResponseEntity.ok(rows);
    }
}
