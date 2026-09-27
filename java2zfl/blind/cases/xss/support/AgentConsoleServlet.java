package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/support/client-info")
public class AgentConsoleServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String userAgent = req.getHeader("User-Agent");
        String language = req.getHeader("Accept-Language");
        String forwarded = req.getHeader("X-Forwarded-For");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<p>Please read the following details to the support agent:</p>");
        out.println("<table class=\"client-info\">");
        out.println("<tr><th>Browser</th><td>" + Encode.forHtml(userAgent) + "</td></tr>");
        out.println("<tr><th>Language</th><td>" + Encode.forHtml(language) + "</td></tr>");
        out.println("<tr><th>Address</th><td>" + Encode.forHtml(forwarded != null ? forwarded : req.getRemoteAddr()) + "</td></tr>");
        out.println("</table>");
    }
}
