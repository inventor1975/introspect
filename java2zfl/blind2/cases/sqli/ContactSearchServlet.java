package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/crm/contacts/search")
public class ContactSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String q = req.getParameter("q");
        if (q == null || q.isBlank()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String escaped = q.trim()
                .replace("\\", "\\\\")
                .replace("%", "\\%")
                .replace("_", "\\_");
        String sql = "SELECT id FROM contacts WHERE full_name LIKE ? ESCAPE '\\' ORDER BY full_name LIMIT 25";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, "%" + escaped + "%");
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getLong(1));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
