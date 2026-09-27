package blind2.sqli;

import blind2.sqli.support.Db;
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

@WebServlet("/products/availability")
public class ProductAvailabilityServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String sku = req.getParameter("sku");
        String storeCode = req.getParameter("store");
        if (sku == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        boolean perStore = storeCode != null && !storeCode.isBlank();
        String sql;
        if (perStore) {
            sql = "SELECT coalesce(sum(qty), 0) FROM store_stock WHERE sku = ? AND store_code = ?";
        } else {
            sql = "SELECT coalesce(sum(qty), 0) FROM store_stock WHERE sku = ?";
        }
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, sku);
            if (perStore) {
                ps.setString(2, storeCode.trim());
            }
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                resp.setContentType("text/plain");
                resp.getWriter().print(rs.getInt(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
