package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/admin/users/role")
public class UserRoleServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session == null || !"ADMIN".equals(session.getAttribute("role"))) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        int userId;
        try {
            userId = Integer.parseInt(req.getParameter("userId"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "invalid user id");
            return;
        }
        String role = req.getParameter("role");

        try (Connection conn = Db.open(); Statement st = conn.createStatement()) {
            int n = st.executeUpdate("UPDATE app_users SET role = '" + role + "', updated_at = now() WHERE id = " + userId);
            resp.setStatus(n == 1 ? HttpServletResponse.SC_OK : HttpServletResponse.SC_NOT_FOUND);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
