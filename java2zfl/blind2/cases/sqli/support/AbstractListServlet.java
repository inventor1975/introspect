package blind2.sqli.support;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.http.HttpServlet;

public abstract class AbstractListServlet extends HttpServlet {

    protected abstract String table();

    protected int countWhere(String condition) throws SQLException {
        String sql = "SELECT count(*) FROM " + table() + " WHERE " + condition;
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            return rs.getInt(1);
        }
    }
}
