package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/search")
public class SearchResultsServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String q = req.getParameter("q");
        if (q == null) {
            q = "";
        }
        String safeQ = StringEscapeUtils.escapeHtml4(q.trim());
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<h2>Results for &ldquo;" + safeQ + "&rdquo;</h2>");
        out.println("<div id=\"results\"></div>");
        out.println("<script>");
        out.println("  var lastQuery = '" + safeQ + "';");
        out.println("  analytics.track('search', { query: lastQuery });");
        out.println("  loadResults(lastQuery);");
        out.println("</script>");
    }
}
