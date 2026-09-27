package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/orders/lookup")
public class OrderLookupServlet extends HttpServlet {

    private static final Logger LOG = Logger.getLogger(OrderLookupServlet.class.getName());

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String orderNo = req.getParameter("orderNo");
        if (orderNo == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String described = "SELECT id, status FROM orders WHERE order_no = '" + orderNo + "'";
        if (LOG.isLoggable(Level.FINE)) {
            LOG.fine("order lookup: " + described.replaceAll("[\\r\\n]", " "));
        }

        String sql = "SELECT id, status FROM orders WHERE order_no = ?";
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, orderNo);
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                    return;
                }
                resp.setContentType("application/json");
                resp.getWriter().print("{\"id\":" + rs.getLong(1) + "}");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
