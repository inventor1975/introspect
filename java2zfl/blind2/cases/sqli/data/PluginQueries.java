package blind2.sqli.data;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.sql.DataSource;

public class PluginQueries {

    private final DataSource dataSource;

    public PluginQueries(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public int countDownloads(String pluginId) throws SQLException {
        return count("SELECT count(*) FROM plugin_downloads WHERE plugin_id = ?", pluginId);
    }

    public int countRatings(String pluginId) throws SQLException {
        return count("SELECT count(*) FROM plugin_ratings WHERE plugin_id = ?", pluginId);
    }

    private int count(String sql, String pluginId) throws SQLException {
        try (Connection conn = dataSource.getConnection(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, pluginId);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getInt(1) : 0;
            }
        }
    }
}
