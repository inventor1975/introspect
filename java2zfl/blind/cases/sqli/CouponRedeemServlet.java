package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/cart/coupon")
public class CouponRedeemServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String raw = request.getParameter("code");
        String code = raw != null ? raw.trim().toUpperCase() : "NONE";
        String cartId = request.getSession().getId();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            int rows = st.executeUpdate("UPDATE coupons SET redeemed_by = 'cart-" + cartId.hashCode()
                    + "' WHERE code = '" + code + "' AND redeemed_by IS NULL");
            response.setStatus(rows == 1 ? HttpServletResponse.SC_OK : HttpServletResponse.SC_NOT_FOUND);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
