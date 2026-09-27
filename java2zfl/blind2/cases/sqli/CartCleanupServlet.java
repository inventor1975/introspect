package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/cart/remove")
public class CartCleanupServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        Object cart = session == null ? null : session.getAttribute("cartId");
        if (!(cart instanceof Long)) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "no active cart");
            return;
        }
        long cartId = (Long) cart;
        String[] skus = req.getParameterValues("sku");
        if (skus == null) {
            resp.sendRedirect(req.getContextPath() + "/cart");
            return;
        }

        try (Connection conn = Db.open(); Statement st = conn.createStatement()) {
            for (String sku : skus) {
                st.addBatch("DELETE FROM cart_items WHERE cart_id = " + cartId + " AND sku = '" + sku + "'");
            }
            st.executeBatch();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.sendRedirect(req.getContextPath() + "/cart");
    }
}
