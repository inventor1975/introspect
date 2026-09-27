package blind.sqli.api;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InvoiceSearchController {

    private static final Map<String, String> FILTER_COLUMNS = Map.of(
            "customer", "customer_id",
            "status", "status",
            "currency", "currency_code");

    private final NamedParameterJdbcTemplate named;

    public InvoiceSearchController(NamedParameterJdbcTemplate named) {
        this.named = named;
    }

    @GetMapping("/api/invoices/search")
    public List<Map<String, Object>> search(@RequestParam Map<String, String> filters) {
        StringBuilder sql = new StringBuilder("SELECT number, customer_id, amount, status FROM invoices WHERE 1 = 1");
        Map<String, Object> params = new HashMap<>();
        for (Map.Entry<String, String> f : filters.entrySet()) {
            String column = FILTER_COLUMNS.get(f.getKey());
            if (column == null) {
                continue;
            }
            sql.append(" AND ").append(column).append(" = :").append(column);
            params.put(column, f.getValue());
        }
        return named.queryForList(sql.append(" ORDER BY number").toString(), params);
    }
}
