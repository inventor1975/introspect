package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.UUID;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/password/reset")
public class PasswordResetServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String raw = req.getParameter("token");
        UUID token;
        try {
            token = UUID.fromString(raw);
        } catch (IllegalArgumentException | NullPointerException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "invalid reset link");
            return;
        }
        String sql = "SELECT user_id FROM password_resets WHERE token = '" + token + "' AND used = false AND expires_at > now()";
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            if (!rs.next()) {
                resp.sendError(HttpServletResponse.SC_NOT_FOUND, "link expired");
                return;
            }
            req.getSession().setAttribute("resetUserId", rs.getLong(1));
            resp.sendRedirect(req.getContextPath() + "/password/new");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
