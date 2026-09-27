package blind2.sqli;

import blind2.sqli.support.DataSources;
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
import javax.servlet.http.HttpSession;
import javax.sql.DataSource;

@WebServlet("/account/orders")
public class OrderHistoryServlet extends HttpServlet {

    private DataSource dataSource;

    @Override
    public void init() throws ServletException {
        dataSource = DataSources.lookup("jdbc/shop");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("customerId") == null) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        long customerId = (Long) session.getAttribute("customerId");

        String sort = req.getParameter("sort");
        if (sort == null || sort.isEmpty()) {
            sort = "placed_at DESC";
        }
        String sql = "SELECT id, total, status FROM orders WHERE customer_id = ? ORDER BY " + sort;

        int rows = 0;
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, customerId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    rows++;
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain");
        resp.getWriter().println("orders: " + rows);
    }
}
