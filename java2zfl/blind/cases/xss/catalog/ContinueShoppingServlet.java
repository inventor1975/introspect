package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/cart/added")
public class ContinueShoppingServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String returnUrl = req.getParameter("returnUrl");
        if (returnUrl == null || returnUrl.isBlank()) {
            returnUrl = "/catalog";
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=\"cart-added\">");
        out.println("<p>The item was added to your cart.</p>");
        out.println("<a class=\"btn\" href=\"" + StringEscapeUtils.escapeHtml4(returnUrl) + "\">Continue shopping</a>");
        out.println("<a class=\"btn primary\" href=\"/checkout\">Checkout</a>");
        out.println("</div>");
    }
}
