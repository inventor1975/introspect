package blind2.sqli;

import blind2.sqli.support.Db;
import blind2.sqli.support.TenantAttributeBinder;
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

@WebServlet("/reports/tenant-revenue")
public class TenantReportServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String tenant = (String) req.getAttribute(TenantAttributeBinder.ATTRIBUTE);
        if (tenant == null) {
            resp.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "tenant not resolved");
            return;
        }
        String sql = "SELECT coalesce(sum(total_cents), 0) FROM invoices WHERE tenant_code = '" + tenant
                + "' AND issued_on >= date_trunc('year', now())";
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.getLong(1));
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
