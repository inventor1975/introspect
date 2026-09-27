package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/table")
public class ReportTableServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String mode = req.getParameter("mode");
        CellFormatter formatter = "rich".equals(mode) ? new PlainCellFormatter() : new EscapingCellFormatter();
        String[] cells = req.getParameterValues("cell");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<table class=\"report\"><tr>");
        if (cells != null) {
            for (String cell : cells) {
                out.println("<td>" + formatter.format(cell) + "</td>");
            }
        }
        out.println("</tr></table>");
    }
}
