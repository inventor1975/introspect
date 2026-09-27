package blind.sqli;

import blind.sqli.support.Db;
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

@WebServlet("/track/*")
public class ShipmentTrackingServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String path = request.getPathInfo();
        if (path == null || path.length() < 2) {
            response.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        String trackingNo = path.substring(1);
        String sql = "SELECT status, location, updated_at FROM shipment_events WHERE tracking_no = '"
                + trackingNo + "' ORDER BY updated_at DESC";
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                response.getWriter().println(rs.getString("status") + " @ " + rs.getString("location"));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
