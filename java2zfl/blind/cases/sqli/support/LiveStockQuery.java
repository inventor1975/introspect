package blind.sqli.support;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;

public class LiveStockQuery implements StockQuery {

    private final JdbcTemplate jdbc;

    public LiveStockQuery(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    public List<Map<String, Object>> findBySku(String sku) {
        return jdbc.queryForList(
                "SELECT sku, warehouse, qty FROM stock_live WHERE sku = ? ORDER BY warehouse", sku);
    }
}
