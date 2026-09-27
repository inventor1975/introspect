package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.MessageFormat;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/shipping/rate")
public class ShippingRateServlet extends HttpServlet {

    private static final String RATE_SQL =
            "SELECT rate_cents FROM shipping_rates WHERE zone = ''{0}'' AND max_weight_g >= {1} ORDER BY max_weight_g LIMIT 1";

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String zone = req.getParameter("zone");
        int grams;
        try {
            grams = Integer.parseInt(req.getParameter("grams"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "grams must be an integer");
            return;
        }
        String sql = MessageFormat.format(RATE_SQL, zone, String.valueOf(grams));
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.next() ? String.valueOf(rs.getInt(1)) : "n/a");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
