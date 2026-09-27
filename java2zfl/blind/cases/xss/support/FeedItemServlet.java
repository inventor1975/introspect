package blind.xss.support;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/support/community/preview")
public class FeedItemServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String title = StringEscapeUtils.escapeXml11(req.getParameter("title"));
        String author = StringEscapeUtils.escapeXml11(req.getParameter("author"));
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<article class=\"post\">");
        out.println("  <h3>" + title + "</h3>");
        out.println("  <p class=\"byline\">Posted by " + author + "</p>");
        out.println("</article>");
    }
}
