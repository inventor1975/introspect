package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/summary-footer")
public class SummaryFooterServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String note = req.getParameter("note");
        String cleaned = note == null ? "" : note.replaceAll("[^A-Za-z0-9 .,-]", "");
        if (cleaned.length() > 120) {
            cleaned = cleaned.substring(0, 120);
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<footer class=\"summary-footer\"><small>" + cleaned + "</small></footer>");
    }
}
