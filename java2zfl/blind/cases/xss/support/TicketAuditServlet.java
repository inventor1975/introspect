package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDate;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/support/tickets/audit")
public class TicketAuditServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String agent = req.getParameter("agent");
        String action = req.getParameter("action");
        String what = "close".equals(action) ? "closed the ticket" : "viewed the ticket";
        TicketFormatter formatter = new TicketFormatter();
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<ul class=\"audit\">");
        out.println(formatter.datedLine(LocalDate.now(), Encode.forHtml(agent), what));
        out.println("</ul>");
    }
}
