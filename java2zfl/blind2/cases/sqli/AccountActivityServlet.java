package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Set;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/activity")
public class AccountActivityServlet extends HttpServlet {

    private static final Set<String> EVENT_TYPES = Set.of("LOGIN", "LOGOUT", "PASSWORD_CHANGE", "MFA_ENROLL");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Object uid = req.getSession().getAttribute("userId");
        if (!(uid instanceof Long)) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        String type = req.getParameter("type");
        String typeFilter;
        if (type != null && EVENT_TYPES.contains(type)) {
            typeFilter = " AND event_type = '" + type + "'";
        } else {
            typeFilter = "";
        }
        String sql = "SELECT occurred_at, ip_hash FROM account_events WHERE user_id = ?" + typeFilter
                + " ORDER BY occurred_at DESC LIMIT 50";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, (Long) uid);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getTimestamp(1));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
