package blind2.sqli.data;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import javax.sql.DataSource;

public class ProductDao {

    private final DataSource dataSource;

    public ProductDao(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<String> findSkusByCategory(String categoryCode) throws SQLException {
        String sql = "SELECT sku FROM products WHERE category_code = '" + categoryCode + "' AND active = true ORDER BY sku";
        List<String> skus = new ArrayList<>();
        try (Connection conn = dataSource.getConnection();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                skus.add(rs.getString(1));
            }
        }
        return skus;
    }

    public List<String> findSkusBySupplier(long supplierId) throws SQLException {
        List<String> skus = new ArrayList<>();
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT sku FROM products WHERE supplier_id = ? AND active = true ORDER BY sku")) {
            ps.setLong(1, supplierId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    skus.add(rs.getString(1));
                }
            }
        }
        return skus;
    }
}
