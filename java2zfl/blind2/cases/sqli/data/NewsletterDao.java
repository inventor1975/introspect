package blind2.sqli.data;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import javax.sql.DataSource;

public class NewsletterDao {

    private final DataSource dataSource;

    public NewsletterDao(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public boolean subscribe(String email, String listCode) throws SQLException {
        String sql = "INSERT INTO newsletter_subscribers(email, list_code, subscribed_at) VALUES (?, ?, now()) ON CONFLICT DO NOTHING";
        try (Connection conn = dataSource.getConnection(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, email);
            ps.setString(2, listCode);
            return ps.executeUpdate() > 0;
        }
    }

    public int unsubscribe(String email) throws SQLException {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement("DELETE FROM newsletter_subscribers WHERE email = ?")) {
            ps.setString(1, email);
            return ps.executeUpdate();
        }
    }
}
