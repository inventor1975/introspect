package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/landing")
public class WelcomeBannerServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String partner = request.getParameter("ref");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        if (partner != null && !partner.isBlank()) {
            out.println("<div class=\"promo\">Welcome, visitors from " + Encode.forHtml(partner.trim()) + "! Enjoy 10% off.</div>");
        }
        out.println("<a href=\"/shop\">Start shopping</a>");
        out.println("</body></html>");
    }
}
