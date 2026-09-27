package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/alerts/price")
public class PriceAlertServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String sku = request.getParameter("sku");
        double threshold;
        try {
            threshold = Double.parseDouble(request.getParameter("below"));
        } catch (NumberFormatException | NullPointerException e) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "below must be a number");
            return;
        }
        if (Double.isNaN(threshold) || Double.isInfinite(threshold)) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String sql = "INSERT INTO price_alerts (sku, threshold, email) VALUES (?, " + threshold + ", ?)";
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, sku);
            ps.setString(2, request.getParameter("email"));
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
