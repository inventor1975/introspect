package blind.sqli.api;

import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrgChartController {

    private static final Map<String, OrgQuery> VIEWS = Map.of(
            "chain", new ManagerChainQuery(),
            "reports", new DirectReportsQuery(),
            "peers", new PeersQuery());

    private final JdbcTemplate jdbc;

    public OrgChartController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/org/{employeeId}")
    public ResponseEntity<List<Map<String, Object>>> view(@PathVariable long employeeId,
                                                          @RequestParam(defaultValue = "reports") String view) {
        OrgQuery query = VIEWS.get(view);
        if (query == null) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(query.run(jdbc, employeeId));
    }
}
