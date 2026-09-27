package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/csv-preview")
public class ReportCsvPreviewServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String csv = req.getParameter("csv");
        CellFormatter formatter = new EscapingCellFormatter();
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<table class=\"csv-preview\">");
        if (csv != null) {
            for (String row : csv.split("\\R")) {
                out.print("<tr>");
                for (String cell : row.split(",", -1)) {
                    out.print("<td>" + formatter.format(cell.trim()) + "</td>");
                }
                out.println("</tr>");
            }
        }
        out.println("</table>");
    }
}
