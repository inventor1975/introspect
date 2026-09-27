package blind.sqli.support;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.JdbcTemplate;

public class LegacyStockQuery implements StockQuery {

    private final JdbcTemplate jdbc;

    public LegacyStockQuery(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    public List<Map<String, Object>> findBySku(String sku) {
        String sql = "SELECT ITEM_NO AS sku, WHS AS warehouse, ON_HAND AS qty FROM LEGACY_INV WHERE ITEM_NO = '"
                + sku + "'";
        return jdbc.queryForList(sql);
    }
}
