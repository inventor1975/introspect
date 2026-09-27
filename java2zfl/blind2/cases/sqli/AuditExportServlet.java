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

@WebServlet("/admin/audit/export")
public class AuditExportServlet extends HttpServlet {

    private String auditTable;

    @Override
    public void init() throws ServletException {
        String configured = getInitParameter("auditTable");
        auditTable = configured == null || configured.isBlank() ? "audit_log" : configured.trim();
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        int days;
        try {
            days = Integer.parseInt(req.getParameter("days"));
        } catch (NumberFormatException e) {
            days = 7;
        }
        days = Math.max(1, Math.min(days, 90));
        String sql = "SELECT id, occurred_at FROM " + auditTable + " WHERE occurred_at > now() - interval '" + days
                + " days' ORDER BY occurred_at";

        resp.setContentType("text/csv");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + "," + rs.getTimestamp(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
