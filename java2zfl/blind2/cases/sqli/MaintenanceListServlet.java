package blind2.sqli;

import blind2.sqli.support.AbstractSortableServlet;
import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/facilities/maintenance")
public class MaintenanceListServlet extends AbstractSortableServlet {

    private static final Map<String, String> COLUMNS = Map.of(
            "due", "due_date",
            "asset", "asset_tag",
            "priority", "priority");

    @Override
    protected Map<String, String> sortColumns() {
        return COLUMNS;
    }

    @Override
    protected String defaultSort() {
        return "due_date";
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        long siteId;
        try {
            siteId = Long.parseLong(req.getParameter("site"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String sql = "SELECT id, priority FROM maintenance_jobs WHERE site_id = ? AND done = false" + orderBy(req);

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, siteId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getLong(1) + " p" + rs.getInt(2));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
