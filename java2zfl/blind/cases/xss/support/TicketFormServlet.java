package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/support/tickets/new")
public class TicketFormServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Map<String, String> form = new LinkedHashMap<>();
        form.put("subject", req.getParameter("subject"));
        form.put("description", req.getParameter("description"));

        List<String> errors = new ArrayList<>();
        if (form.get("subject") == null || form.get("subject").isBlank()) {
            errors.add("Subject is required.");
        }
        if (form.get("description") == null || form.get("description").length() < 20) {
            errors.add("Please describe the problem in at least 20 characters.");
        }
        if (errors.isEmpty()) {
            resp.sendRedirect("/support/tickets");
            return;
        }

        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<ul class=\"errors\">");
        for (String error : errors) {
            out.println("<li>" + error + "</li>");
        }
        out.println("</ul>");
        out.println("<form method=\"post\">");
        out.println("  <input name=\"subject\" value=\"" + form.getOrDefault("subject", "") + "\">");
        out.println("  <textarea name=\"description\"></textarea>");
        out.println("</form>");
    }
}
