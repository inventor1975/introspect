package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.util.HtmlUtils;

@WebServlet("/reports/notes")
public class ReportExportServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String format = request.getParameter("format");
        String note = request.getParameter("note");
        if (note == null) {
            note = "";
        }
        String rendered;
        if ("html".equals(format)) {
            rendered = "<pre>" + HtmlUtils.htmlEscape(note) + "</pre>";
        } else {
            rendered = "<div class=\"note\">" + note.replace("\n", "<br>") + "</div>";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2>Report note</h2>");
        out.println(rendered);
        out.println("</body></html>");
    }
}
