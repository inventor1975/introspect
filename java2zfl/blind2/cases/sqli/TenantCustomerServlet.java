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

@WebServlet("/internal/customers/new-count")
public class TenantCustomerServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String schema = req.getHeader("X-Tenant");
        if (schema == null || schema.isBlank()) {
            schema = "public";
        }
        String sql = "SELECT count(*) FROM " + schema + ".customers WHERE created_at > now() - interval '30 days'";
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            rs.next();
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.getInt(1));
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
