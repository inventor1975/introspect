package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/cart/quantity")
public class OrderQuantityServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String raw = request.getParameter("qty");
        int qty;
        try {
            qty = Integer.parseInt(raw.trim());
        } catch (RuntimeException e) {
            qty = 1;
        }
        if (qty < 1) {
            qty = 1;
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<p>Quantity updated to <b>" + qty + "</b>.</p>");
        out.println("<input type=\"number\" name=\"qty\" value=\"" + qty + "\">");
        out.println("</body></html>");
    }
}
