package blind.sqli.api;

import java.util.List;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PayrollController {

    private static final String[] COST_CENTER_HEADERS = {"X-Cost-Center", "X-CC", "X-Department-Code"};

    private final JdbcTemplate jdbc;

    public PayrollController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/payroll/runs")
    public List<Map<String, Object>> runs(HttpServletRequest request) {
        String costCenter = "CC-000";
        for (String h : COST_CENTER_HEADERS) {
            String v = request.getHeader(h);
            if (v != null && !v.isBlank()) {
                costCenter = v;
                break;
            }
        }
        return jdbc.queryForList("SELECT run_id, period, gross_total FROM payroll_runs WHERE cost_center = '"
                + costCenter + "' ORDER BY period DESC");
    }
}
