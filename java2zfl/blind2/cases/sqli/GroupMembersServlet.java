package blind2.sqli;

import static blind2.sqli.data.Tables.GROUPS;
import static blind2.sqli.data.Tables.MEMBERSHIPS;
import static blind2.sqli.data.Tables.USERS;

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

@WebServlet("/groups/members")
public class GroupMembersServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String group = req.getParameter("group");
        if (group == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String sql = "SELECT u.id FROM " + USERS + " u"
                + " JOIN " + MEMBERSHIPS + " m ON m.user_id = u.id"
                + " JOIN " + GROUPS + " g ON g.id = m.group_id"
                + " WHERE g.slug = ? ORDER BY u.id";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, group);
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
