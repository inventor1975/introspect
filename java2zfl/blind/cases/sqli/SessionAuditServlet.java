package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/audit/visit")
public class SessionAuditServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String trackingId = "unknown";
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("trk".equals(c.getName())) {
                    trackingId = c.getValue();
                    break;
                }
            }
        }
        String page = request.getRequestURI();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            st.executeUpdate("INSERT INTO visit_log (tracking_id, page, seen_at) VALUES ('"
                    + trackingId + "', '" + page.length() + "', CURRENT_TIMESTAMP)");
        } catch (SQLException e) {
            log("could not record visit: " + e.getMessage());
        }
        response.setStatus(HttpServletResponse.SC_OK);
    }

    private void log(String message) {
        System.err.println(message);
    }
}
