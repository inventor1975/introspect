package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

/**
 * Landing page for a marketing campaign. Each campaign servlet provides its name and may customise how the
 * redeemed code text is prepared for display.
 */
public abstract class PromoServletBase extends HttpServlet {

    protected abstract String campaignName();

    protected String formatCode(String code) {
        return Encode.forHtml(code);
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String code = req.getParameter("code");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<section class=\"promo\">");
        out.println("<h2>" + campaignName() + "</h2>");
        if (code != null && !code.isEmpty()) {
            out.println("<p>Your code: <strong>" + formatCode(code) + "</strong></p>");
        } else {
            out.println("<p>Enter a code at checkout to redeem this offer.</p>");
        }
        out.println("</section>");
    }
}
