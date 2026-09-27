package blind2.sqli;

import java.util.List;
import java.util.Locale;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InventoryReportController {

    private final JdbcTemplate jdbc;

    public InventoryReportController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/inventory/report")
    public List<Map<String, Object>> report(@RequestParam(value = "groupBy", defaultValue = "sku") String groupBy) {
        String column = switch (groupBy.toLowerCase(Locale.ROOT)) {
            case "warehouse" -> "warehouse_code";
            case "supplier" -> "supplier_id";
            case "category" -> "category_code";
            default -> "sku";
        };
        return jdbc.queryForList("SELECT " + column + " AS bucket, sum(qty) AS qty FROM stock GROUP BY " + column
                + " ORDER BY 2 DESC LIMIT 100");
    }
}
