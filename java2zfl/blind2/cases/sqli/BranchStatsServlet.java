package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/branches/request-stats")
public class BranchStatsServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String view = req.getParameter("view");
        long count;
        try (Connection conn = Db.open()) {
            if ("closed".equals(view)) {
                count = countByStatus(conn, "CLOSED");
            } else if ("pending".equals(view)) {
                count = countByStatus(conn, "PENDING");
            } else {
                count = countByStatus(conn, "OPEN");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain");
        resp.getWriter().print(count);
    }

    private long countByStatus(Connection conn, String status) throws SQLException {
        try (Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT count(*) FROM branch_requests WHERE status = '" + status + "'")) {
            rs.next();
            return rs.getLong(1);
        }
    }
}
