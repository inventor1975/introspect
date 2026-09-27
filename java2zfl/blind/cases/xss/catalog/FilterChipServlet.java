package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/catalog/filters")
public class FilterChipServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String[] filters = req.getParameterValues("filter");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=chips>");
        if (filters != null) {
            for (String f : filters) {
                out.println("<button type=button class=chip data-filter=" + Encode.forHtmlAttribute(f) + ">"
                        + Encode.forHtml(f) + " &times;</button>");
            }
        }
        out.println("</div>");
    }
}
