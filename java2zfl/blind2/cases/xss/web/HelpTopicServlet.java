package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Map;

@WebServlet("/help")
public class HelpTopicServlet extends HttpServlet {

    private static final Map<String, String> TOPICS = Map.of(
            "billing", "<p>Invoices are issued on the first of each month.</p>",
            "shipping", "<p>Orders ship within two business days.</p>",
            "returns", "<p>You can return items within 30 days.</p>");

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String topic = request.getParameter("topic");
        String body = TOPICS.getOrDefault(topic == null ? "" : topic.toLowerCase(), "<p>Topic not found.</p>");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2>Help</h2>");
        out.println(body);
        out.println("</body></html>");
    }
}
