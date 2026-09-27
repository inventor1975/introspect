package blind2.sqli.data;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class TransferDao {

    private final JdbcTemplate jdbc;

    public TransferDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public int recordTransfer(String fromWarehouse, String toWarehouse, String sku, int quantity) {
        return jdbc.update(
                "INSERT INTO stock_transfers(from_wh, to_wh, sku, qty, created_at) VALUES (?, ?, ?, ?, now())",
                fromWarehouse, toWarehouse, sku, quantity);
    }
}
