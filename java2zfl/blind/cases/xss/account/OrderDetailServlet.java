package blind.xss.account;

import blind.xss.common.BasePageServlet;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/order")
public class OrderDetailServlet extends BasePageServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String orderNo = req.getParameter("order");
        long orderId;
        try {
            orderId = Long.parseLong(orderNo);
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        String body = "<p>Loading order details&hellip;</p>"
                + "<div id=\"order\" data-order-id=\"" + orderId + "\"></div>";
        render(resp, "Order " + orderNo, body);
    }
}
