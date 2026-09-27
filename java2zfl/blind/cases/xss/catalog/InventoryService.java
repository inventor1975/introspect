package blind.xss.catalog;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;

@Service
public class InventoryService {

    private final Map<String, Integer> stockBySku = new ConcurrentHashMap<>();

    public void record(String sku, int quantity) {
        stockBySku.put(sku, quantity);
    }

    /** Short HTML status line for a SKU, used in the storefront and the back office. */
    public String describe(String sku) {
        Integer quantity = stockBySku.get(sku);
        if (quantity == null) {
            return "<span class=\"stock missing\">SKU <b>" + sku + "</b> is not carried in this store</span>";
        }
        return describeLevel(quantity);
    }

    public String describeLevel(int quantity) {
        if (quantity <= 0) {
            return "<span class=\"stock out\">Out of stock</span>";
        }
        if (quantity < 5) {
            return "<span class=\"stock low\">Only " + quantity + " left</span>";
        }
        return "<span class=\"stock ok\">In stock (" + quantity + ")</span>";
    }
}
