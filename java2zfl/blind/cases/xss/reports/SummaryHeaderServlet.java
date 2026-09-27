package blind.xss.reports;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/summary-header")
public class SummaryHeaderServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String heading = req.getParameter("heading");
        heading = heading == null ? "summary" : heading.trim();
        String normalized = heading.replace('_', ' ');
        if (!normalized.isEmpty()) {
            normalized = Character.toUpperCase(normalized.charAt(0)) + normalized.substring(1);
        }
        resp.setContentType("text/html;charset=UTF-8");
        resp.getWriter()
                .append("<h1 class=\"summary\">")
                .append(normalized)
                .append("</h1>");
    }
}
