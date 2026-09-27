package blind2.sqli.data;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.sql.DataSource;

public class MaintenanceActions {

    private final DataSource dataSource;

    public MaintenanceActions(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public int purgeSessionsFor(String login) throws SQLException {
        try (Connection conn = dataSource.getConnection(); Statement st = conn.createStatement()) {
            return st.executeUpdate("DELETE FROM web_sessions WHERE login = '" + login + "'");
        }
    }

    public int unlockAccount(String login) throws SQLException {
        try (Connection conn = dataSource.getConnection(); Statement st = conn.createStatement()) {
            return st.executeUpdate("UPDATE accounts SET failed_logins = 0, locked = false WHERE login = '" + login + "'");
        }
    }
}
