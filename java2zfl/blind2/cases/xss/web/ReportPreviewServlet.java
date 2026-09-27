package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.util.HtmlUtils;

@WebServlet("/reports/preview")
public class ReportPreviewServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String layout = request.getParameter("layout");
        String caption = request.getParameter("caption");
        String block;
        if ("compact".equals(layout)) {
            block = "<small>" + HtmlUtils.htmlEscape(caption == null ? "" : caption) + "</small>";
        } else if (caption == null || caption.isBlank()) {
            block = "<h3>Untitled report</h3>";
        } else {
            String escaped = HtmlUtils.htmlEscape(caption);
            block = "<h3>" + escaped + "</h3>";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>" + block + "<div id=\"chart\"></div></body></html>");
    }
}
