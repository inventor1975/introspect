package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/support/tickets/summary")
public class TicketSummaryServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Map<String, String> summary = new HashMap<>();
        summary.put("subject", req.getParameter("subject"));
        summary.put("status", "Open");
        summary.put("queue", "General enquiries");

        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<dl class=\"ticket\">");
        out.println("<dt>Status</dt><dd>" + summary.get("status") + "</dd>");
        out.println("<dt>Queue</dt><dd>" + summary.get("queue") + "</dd>");
        out.println("<dt>Subject</dt><dd>" + Encode.forHtml(summary.get("subject")) + "</dd>");
        out.println("</dl>");
    }
}
