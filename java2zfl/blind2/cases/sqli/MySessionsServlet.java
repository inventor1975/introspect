package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/account/sessions")
public class MySessionsServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        Long uid = session == null ? null : (Long) session.getAttribute("uid");
        if (uid == null) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        String sql = "SELECT id, created_at, last_seen_at FROM web_sessions WHERE user_id = " + uid
                + " AND revoked = false ORDER BY last_seen_at DESC";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + "\t" + rs.getTimestamp(2) + "\t" + rs.getTimestamp(3));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
