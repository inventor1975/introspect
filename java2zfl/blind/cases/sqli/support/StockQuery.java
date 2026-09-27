package blind.sqli.support;

import java.util.List;
import java.util.Map;

public interface StockQuery {
    List<Map<String, Object>> findBySku(String sku);
}
