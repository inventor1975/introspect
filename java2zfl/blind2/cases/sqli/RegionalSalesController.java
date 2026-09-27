package blind2.sqli;

import blind2.sqli.support.ReportContext;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RegionalSalesController {

    private final JdbcTemplate jdbc;

    public RegionalSalesController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/sales/monthly")
    public List<Map<String, Object>> monthly() {
        String region = ReportContext.region();
        String filter = region == null || "GLOBAL".equals(region) ? "" : " WHERE region = '" + region + "'";
        return jdbc.queryForList("SELECT date_trunc('month', sold_on) AS month, sum(amount) AS total FROM sales"
                + filter + " GROUP BY 1 ORDER BY 1");
    }
}
