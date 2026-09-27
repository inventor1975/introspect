package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/catalog/sort")
public class SortLinkServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String sort = req.getParameter("sort");
        if (sort == null) {
            sort = "relevance";
        }
        String attr = Encode.forHtmlAttribute(sort);
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=\"sort\" data-current=\"" + attr + "\">");
        out.println("  <a href=\"/catalog?sort=" + attr + "&amp;dir=asc\">Ascending</a>");
        out.println("  <a href=\"/catalog?sort=" + attr + "&amp;dir=desc\">Descending</a>");
        out.println("</div>");
    }
}
