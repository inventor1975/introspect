package blind.sqli.api;

import blind.sqli.support.ArchivedStockQuery;
import blind.sqli.support.LegacyStockQuery;
import blind.sqli.support.StockQuery;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InventoryController {

    private final JdbcTemplate jdbc;

    public InventoryController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/api/inventory/{sku}")
    public List<Map<String, Object>> stock(@PathVariable String sku,
                                           @RequestParam(defaultValue = "legacy") String source) {
        StockQuery query = "archive".equals(source) ? new ArchivedStockQuery(jdbc) : new LegacyStockQuery(jdbc);
        return query.findBySku(sku);
    }
}
