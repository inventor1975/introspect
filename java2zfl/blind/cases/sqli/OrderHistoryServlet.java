package blind.sqli;

import blind.sqli.support.Db;
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

@WebServlet("/orders/history")
public class OrderHistoryServlet extends HttpServlet {

    private static final String ORDERS_TABLE = "orders";
    private static final String COLUMNS = "id, placed_at, total, status";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String customer = request.getParameter("customer");
        String status = request.getParameter("status");
        if (customer == null || customer.isBlank()) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "customer is required");
            return;
        }
        String sql = "SELECT " + COLUMNS + " FROM " + ORDERS_TABLE + " WHERE customer_name = ?"
                + (status != null ? " AND status = ?" : "") + " ORDER BY placed_at DESC";
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, customer);
            if (status != null) {
                ps.setString(2, status);
            }
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getLong("id") + "\t" + rs.getString("status") + "\t" + rs.getBigDecimal("total"));
                }
            }
        } catch (SQLException e) {
            throw new ServletException("order history failed", e);
        }
    }
}
