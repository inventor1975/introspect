package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/widgets/product")
public class ProductWidgetServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String title = req.getParameter("title");
        if (title == null) {
            title = "Featured product";
        }
        String jsSafe = StringEscapeUtils.escapeEcmaScript(title);
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=\"widget\">");
        out.println("  <h3>" + jsSafe + "</h3>");
        out.println("  <script>ProductWidget.init(\"" + jsSafe + "\");</script>");
        out.println("</div>");
    }
}
