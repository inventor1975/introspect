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

@WebServlet("/projects")
public class ArchiveToggleServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String archivedFlag = req.getParameter("archived");
        boolean archived = Boolean.parseBoolean(archivedFlag);
        String sql = "SELECT id, member_count FROM projects WHERE archived = " + archived + " ORDER BY updated_at DESC";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + " (" + rs.getInt(2) + " members)");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
