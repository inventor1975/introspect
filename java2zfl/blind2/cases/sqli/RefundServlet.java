package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/orders/refund")
public class RefundServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        long orderId;
        try {
            orderId = Long.parseLong(req.getParameter("orderId"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String reason = req.getParameter("reason");
        if (reason == null || reason.isBlank()) {
            reason = "OTHER";
        }
        try (Connection conn = Db.open();
             PreparedStatement ps = prepare(conn,
                     "INSERT INTO refund_requests(order_id, reason_code, requested_at) VALUES (?, '" + reason + "', now())",
                     orderId)) {
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setStatus(HttpServletResponse.SC_OK);
    }

    private static PreparedStatement prepare(Connection conn, String sql, Object... args) throws SQLException {
        PreparedStatement ps = conn.prepareStatement(sql);
        for (int i = 0; i < args.length; i++) {
            ps.setObject(i + 1, args[i]);
        }
        return ps;
    }
}
