package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/search/empty")
public class ButtonActionServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String term = request.getParameter("term");
        String escaped = StringEscapeUtils.escapeHtml4(term == null ? "" : term);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<p>No results for <em>" + escaped + "</em>.</p>");
        out.println("<button onclick=\"retrySearch('" + escaped + "', {fuzzy: true})\">Try fuzzy search</button>");
        out.println("<script src=\"/static/search.js\"></script></body></html>");
    }
}
