package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/invoices/lookup")
public class InvoiceLookupServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String tenant = request.getHeader("X-Tenant-Id");
        String number = request.getParameter("number");
        if (tenant == null) {
            tenant = "public";
        }
        String sql = "SELECT number, issued_on, amount FROM " + tenant.toLowerCase() + ".invoices WHERE number = ?";
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, number);
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    response.sendError(HttpServletResponse.SC_NOT_FOUND);
                    return;
                }
                response.getWriter().println(rs.getString("number") + " " + rs.getBigDecimal("amount"));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
