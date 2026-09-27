package blind2.sqli.data;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Optional;
import javax.sql.DataSource;

public class JdbcCustomerRepository implements CustomerRepository {

    private static final String COLUMNS = "id, email, tier";

    private final DataSource dataSource;

    public JdbcCustomerRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Optional<CustomerRecord> findByEmail(String email) throws SQLException {
        String sql = "SELECT " + COLUMNS + " FROM customers WHERE lower(email) = lower('" + email + "')";
        try (Connection conn = dataSource.getConnection();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            return rs.next() ? Optional.of(map(rs)) : Optional.empty();
        }
    }

    @Override
    public Optional<CustomerRecord> findById(long id) throws SQLException {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT " + COLUMNS + " FROM customers WHERE id = ?")) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? Optional.of(map(rs)) : Optional.empty();
            }
        }
    }

    private static CustomerRecord map(ResultSet rs) throws SQLException {
        return new CustomerRecord(rs.getLong("id"), rs.getString("email"), rs.getString("tier"));
    }
}
