package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/consent/record")
public class CookieConsentServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String consent = null;
        String visitor = null;
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("consent".equals(c.getName())) {
                    consent = c.getValue();
                } else if ("vid".equals(c.getName())) {
                    visitor = c.getValue();
                }
            }
        }
        String flag = "accepted".equals(consent) ? "1" : "0";
        String sql = "UPDATE visitors SET analytics_ok = " + flag + ", consent_at = CURRENT_TIMESTAMP WHERE visitor_id = ?";
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, visitor);
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        response.setStatus(HttpServletResponse.SC_OK);
    }
}
