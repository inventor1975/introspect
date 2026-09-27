package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/inventory/count")
public class InventoryCountServlet extends HttpServlet {

    private static final String UPSERT = "INSERT INTO cycle_counts (bin_code, sku, counted_qty) VALUES (?, ?, ?)"
            + " ON CONFLICT (bin_code, sku) DO UPDATE SET counted_qty = EXCLUDED.counted_qty";

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String bin = request.getParameter("bin");
        Map<String, String[]> params = request.getParameterMap();
        try (Connection conn = Db.connect(); PreparedStatement ps = conn.prepareStatement(UPSERT)) {
            for (Map.Entry<String, String[]> e : params.entrySet()) {
                if (!e.getKey().startsWith("sku:")) {
                    continue;
                }
                ps.setString(1, bin);
                ps.setString(2, e.getKey().substring(4));
                ps.setString(3, e.getValue()[0]);
                ps.addBatch();
            }
            ps.executeBatch();
        } catch (SQLException ex) {
            throw new ServletException(ex);
        }
        response.sendRedirect("/inventory/bins/" + bin.hashCode());
    }
}
