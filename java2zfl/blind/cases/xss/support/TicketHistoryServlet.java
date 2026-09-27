package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/support/tickets/comment-preview")
public class TicketHistoryServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String agent = req.getParameter("agent");
        String comment = req.getParameter("comment");
        TicketFormatter formatter = new TicketFormatter();
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<ul class=\"history\">");
        out.println(formatter.line(Encode.forHtml(agent), "commented: " + comment));
        out.println("</ul>");
    }
}
