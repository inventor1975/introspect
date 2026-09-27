package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Locale;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/checkout/coupon/check")
public class CouponCodeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String code = req.getParameter("code");
        if (code == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String normalized = code.replaceAll("[^A-Za-z0-9]", "").toUpperCase(Locale.ROOT);
        if (normalized.isEmpty()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT discount_pct FROM coupons WHERE code = '" + normalized
                     + "' AND valid_until >= current_date")) {
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.next() ? rs.getInt(1) : 0);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
