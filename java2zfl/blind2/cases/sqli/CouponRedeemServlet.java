package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.lang3.StringUtils;

@WebServlet("/checkout/coupon")
public class CouponRedeemServlet extends HttpServlet {

    private static final Logger LOG = Logger.getLogger(CouponRedeemServlet.class.getName());

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String code = StringUtils.trim(req.getParameter("code"));
        String orderId = req.getParameter("orderId");
        if (!StringUtils.isNumeric(orderId)) {
            LOG.warning("coupon redeem with unexpected order id format");
        }

        try (Connection conn = Db.open();
             PreparedStatement ps = conn.prepareStatement(
                     "UPDATE orders SET coupon_code = ? WHERE id = " + orderId + " AND status = 'CART'")) {
            ps.setString(1, code);
            int n = ps.executeUpdate();
            resp.setStatus(n == 1 ? HttpServletResponse.SC_OK : HttpServletResponse.SC_NOT_FOUND);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
