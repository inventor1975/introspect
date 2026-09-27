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

@WebServlet("/warehouse/adjust")
public class InventoryAdjustServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String sku = req.getParameter("sku");
        String delta = req.getParameter("delta");
        if (sku == null || delta == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        delta = delta.replace("'", "").replace("\"", "").trim();

        try (Connection conn = Db.open();
             PreparedStatement ps = conn.prepareStatement("UPDATE stock SET qty = qty + " + delta + ", adjusted_at = now() WHERE sku = ?")) {
            ps.setString(1, sku);
            int n = ps.executeUpdate();
            resp.setStatus(n > 0 ? HttpServletResponse.SC_OK : HttpServletResponse.SC_NOT_FOUND);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
