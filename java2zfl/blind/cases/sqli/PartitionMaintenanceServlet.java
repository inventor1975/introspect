package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/ops/partitions/mark")
public class PartitionMaintenanceServlet extends HttpServlet {

    private String eventsTable;

    @Override
    public void init() throws ServletException {
        String configured = getInitParameter("eventsTable");
        eventsTable = configured != null ? configured : "events_current";
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String batchId = request.getParameter("batch");
        String sql = "UPDATE " + eventsTable + " SET reprocess = TRUE WHERE batch_id = ?";
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, batchId);
            response.getWriter().println(ps.executeUpdate() + " rows marked");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
