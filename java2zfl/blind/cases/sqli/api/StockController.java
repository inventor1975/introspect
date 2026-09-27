package blind.sqli.api;

import blind.sqli.support.ArchivedStockQuery;
import blind.sqli.support.LiveStockQuery;
import blind.sqli.support.StockQuery;
import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StockController {

    private final StockQuery live;
    private final StockQuery archive;

    public StockController(JdbcTemplate jdbc) {
        this.live = new LiveStockQuery(jdbc);
        this.archive = new ArchivedStockQuery(jdbc);
    }

    @GetMapping("/api/v2/inventory/{sku}")
    public List<Map<String, Object>> stock(@PathVariable String sku,
                                           @RequestParam(defaultValue = "live") String source) {
        StockQuery query = "archive".equals(source) ? archive : live;
        return query.findBySku(sku);
    }
}
