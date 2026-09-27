package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/account/display-name")
public class DisplayNameServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        Object uid = session == null ? null : session.getAttribute("userId");
        if (!(uid instanceof Long)) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        String name = req.getParameter("displayName");
        if (name == null || name.isBlank() || name.length() > 60) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "display name must be 1-60 characters");
            return;
        }
        try (Connection conn = Db.open();
             PreparedStatement ps = conn.prepareStatement("UPDATE users SET display_name = ?, updated_at = now() WHERE id = ?")) {
            ps.setString(1, name.trim());
            ps.setLong(2, (Long) uid);
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.sendRedirect(req.getContextPath() + "/account");
    }
}
