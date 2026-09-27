package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/account/my-notes")
public class OrderNoteReportServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        Object uid = session == null ? null : session.getAttribute("userId");
        if (!(uid instanceof Long)) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open()) {
            String displayName = null;
            try (PreparedStatement ps = conn.prepareStatement("SELECT display_name FROM users WHERE id = ?")) {
                ps.setLong(1, (Long) uid);
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        displayName = rs.getString(1);
                    }
                }
            }
            if (displayName == null) {
                resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                return;
            }
            try (Statement st = conn.createStatement();
                 ResultSet rs = st.executeQuery("SELECT order_id, created_at FROM order_notes WHERE author_name = '"
                         + displayName + "' ORDER BY created_at DESC")) {
                while (rs.next()) {
                    out.println(rs.getLong(1) + "\t" + rs.getTimestamp(2));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
