package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/support/ticket-actions")
public class TicketActionServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String ref = req.getParameter("ref");
        if (ref == null) {
            ref = "";
        }
        String safeRef = Encode.forHtml(ref);
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=\"actions\">");
        out.println("  <button type=\"button\" onclick=\"openTicket('" + safeRef + "')\">Open " + safeRef + "</button>");
        out.println("  <button type=\"button\" onclick=\"closeTicket('" + safeRef + "')\">Close</button>");
        out.println("</div>");
    }
}
