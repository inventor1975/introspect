package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/admin/purge-sessions")
public class AdminPurgeServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String raw = request.getParameter("olderThanDays");
        String interval;
        try {
            int days = Integer.parseInt(raw);
            interval = "'" + days + " days'";
        } catch (NumberFormatException e) {
            // allow expressions such as '2 weeks' from the admin console
            interval = "'" + raw + "'";
        }
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            int purged = st.executeUpdate(
                    "DELETE FROM web_sessions WHERE last_seen < NOW() - INTERVAL " + interval);
            response.getWriter().println("purged " + purged);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
