package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/search/suggest")
public class SearchSuggestServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String q = req.getParameter("q");
        if (q == null) {
            q = "";
        }
        q = q.trim();
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<h2>Did you mean &ldquo;" + Encode.forHtml(q) + "&rdquo;?</h2>");
        out.println("<ul id=\"suggestions\"></ul>");
        out.println("<script>");
        out.println("  var lastQuery = '" + Encode.forJavaScript(q) + "';");
        out.println("  loadSuggestions(lastQuery);");
        out.println("</script>");
    }
}
