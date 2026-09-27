package blind.sqli.support;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;

public class ArchivedStockQuery implements StockQuery {

    private static final String TABLE = "stock_archive";
    private final JdbcTemplate jdbc;

    public ArchivedStockQuery(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    public List<Map<String, Object>> findBySku(String sku) {
        String sql = "SELECT sku, warehouse, qty, archived_at FROM " + TABLE
                + " WHERE sku = ? ORDER BY archived_at DESC";
        return jdbc.queryForList(sql, sku.toUpperCase());
    }
}
