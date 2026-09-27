package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.BufferedReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/api/shipments/track")
public class ShipmentTrackingServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        StringBuilder body = new StringBuilder();
        try (BufferedReader reader = req.getReader()) {
            String line;
            while ((line = reader.readLine()) != null) {
                body.append(line);
            }
        }
        String trackingNo = jsonField(body.toString(), "trackingNumber");
        if (trackingNo == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "trackingNumber missing");
            return;
        }

        String sql = "SELECT status_code, updated_at FROM shipments WHERE tracking_no = '" + trackingNo + "'";
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            resp.setContentType("application/json");
            if (rs.next()) {
                resp.getWriter().print("{\"status\":" + rs.getInt(1) + "}");
            } else {
                resp.setStatus(HttpServletResponse.SC_NOT_FOUND);
                resp.getWriter().print("{}");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    private static String jsonField(String json, String field) {
        String key = "\"" + field + "\"";
        int k = json.indexOf(key);
        if (k < 0) {
            return null;
        }
        int colon = json.indexOf(':', k + key.length());
        int start = json.indexOf('"', colon + 1);
        int end = start < 0 ? -1 : json.indexOf('"', start + 1);
        return (colon < 0 || start < 0 || end < 0) ? null : json.substring(start + 1, end);
    }
}
