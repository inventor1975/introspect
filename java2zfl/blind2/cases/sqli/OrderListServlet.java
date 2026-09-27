package blind2.sqli;

import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.sql.DataSource;

@WebServlet("/account/order-list")
public class OrderListServlet extends HttpServlet {

    private static final Map<String, String> SORT_COLUMNS = Map.of(
            "date", "placed_at",
            "total", "total_cents",
            "status", "status");

    private DataSource dataSource;

    @Override
    public void init() throws ServletException {
        dataSource = DataSources.lookup("jdbc/shop");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session == null || !(session.getAttribute("customerId") instanceof Long)) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        long customerId = (Long) session.getAttribute("customerId");

        String sortKey = req.getParameter("sort");
        String column = SORT_COLUMNS.getOrDefault(sortKey == null ? "" : sortKey, "placed_at");
        String direction = "asc".equalsIgnoreCase(req.getParameter("dir")) ? "ASC" : "DESC";
        String sql = "SELECT id, total_cents FROM orders WHERE customer_id = ? ORDER BY " + column + " " + direction;

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = dataSource.getConnection(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, customerId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getLong(1) + "\t" + rs.getLong(2));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
