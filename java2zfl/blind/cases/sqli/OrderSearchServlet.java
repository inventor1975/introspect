package blind.sqli;

import blind.sqli.support.Db;
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

@WebServlet("/orders/search")
public class OrderSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String customer = request.getParameter("customer");
        if (customer == null || customer.isBlank()) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "customer is required");
            return;
        }
        String sql = "SELECT id, placed_at, total FROM orders WHERE customer_name = '" + customer
                + "' ORDER BY placed_at DESC";
        response.setContentType("text/plain");
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong("id") + "\t" + rs.getTimestamp("placed_at") + "\t" + rs.getBigDecimal("total"));
            }
        } catch (SQLException e) {
            throw new ServletException("order search failed", e);
        }
    }
}
