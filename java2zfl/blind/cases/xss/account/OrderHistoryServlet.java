package blind.xss.account;

import blind.xss.common.BasePageServlet;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/orders")
public class OrderHistoryServlet extends BasePageServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String status = req.getParameter("status");
        if (status == null || status.isEmpty()) {
            status = "all";
        }
        String body = "<p>Showing orders with status <strong>" + status + "</strong>.</p>"
                + "<ul id=\"orders\" data-endpoint=\"/api/orders\"></ul>";
        render(resp, "Order history", body);
    }
}
