package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Base64;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/auth/resume")
public class RememberMeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String cookieValue = null;
        Cookie[] cookies = req.getCookies();
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("remember".equals(c.getName())) {
                    cookieValue = c.getValue();
                }
            }
        }
        if (cookieValue == null) {
            resp.sendRedirect(req.getContextPath() + "/login");
            return;
        }
        String decoded;
        try {
            decoded = new String(Base64.getDecoder().decode(cookieValue), StandardCharsets.UTF_8);
        } catch (IllegalArgumentException e) {
            resp.sendRedirect(req.getContextPath() + "/login");
            return;
        }
        int sep = decoded.indexOf(':');
        if (sep < 1) {
            resp.sendRedirect(req.getContextPath() + "/login");
            return;
        }
        String series = decoded.substring(0, sep);
        String token = decoded.substring(sep + 1);

        try (Connection conn = Db.open();
             PreparedStatement ps = conn.prepareStatement(
                     "SELECT user_id FROM remember_tokens WHERE series = ? AND token = ? AND expires_at > now()")) {
            ps.setString(1, series);
            ps.setString(2, token);
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    resp.sendRedirect(req.getContextPath() + "/login");
                    return;
                }
                req.getSession().setAttribute("userId", rs.getLong(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.sendRedirect(req.getContextPath() + "/home");
    }
}
