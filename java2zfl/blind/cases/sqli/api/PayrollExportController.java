package blind.sqli.api;

import java.util.List;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PayrollExportController {

    private static final String[] COST_CENTER_HEADERS = {"X-Cost-Center", "X-CC", "X-Department-Code"};
    private static final String RUNS = "SELECT run_id, period, gross_total FROM payroll_runs";

    private final JdbcTemplate jdbc;

    public PayrollExportController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/v2/payroll/runs")
    public List<Map<String, Object>> runs(HttpServletRequest request) {
        String costCenter = null;
        for (String h : COST_CENTER_HEADERS) {
            String v = request.getHeader(h);
            if (v != null && !v.isBlank()) {
                costCenter = v;
                break;
            }
        }
        if (costCenter == null) {
            return jdbc.queryForList(RUNS + " ORDER BY period DESC LIMIT 12");
        }
        return jdbc.queryForList(RUNS + " WHERE cost_center = ? ORDER BY period DESC", costCenter);
    }
}
