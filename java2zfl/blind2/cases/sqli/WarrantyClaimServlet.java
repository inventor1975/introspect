package blind2.sqli;

import blind2.sqli.support.Db;
import blind2.sqli.support.Params;
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

@WebServlet("/service/warranty")
public class WarrantyClaimServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        int productId = Params.integer(req, "productId", -1);
        String serial = Params.text(req, "serial", null);
        if (productId < 0 || serial == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String sql = "SELECT id, status_code FROM warranty_claims WHERE product_id = " + productId + " AND serial_no = ?";
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, serial);
            try (ResultSet rs = ps.executeQuery()) {
                resp.setContentType("text/plain");
                resp.getWriter().print(rs.next() ? rs.getLong(1) + ":" + rs.getInt(2) : "none");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
