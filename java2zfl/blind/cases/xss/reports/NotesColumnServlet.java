package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/row-preview")
public class NotesColumnServlet extends HttpServlet {

    private static final List<String> COLUMNS = List.of("customer", "amount", "notes");

    private static final Map<String, CellFormatter> FORMATTERS = Map.of(
            "customer", new EscapingCellFormatter(),
            "amount", new CurrencyCellFormatter(),
            "notes", new PlainCellFormatter());

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.print("<table class=\"report\"><tr>");
        for (String column : COLUMNS) {
            CellFormatter formatter = FORMATTERS.get(column);
            out.print("<td class=\"" + column + "\">" + formatter.format(req.getParameter(column)) + "</td>");
        }
        out.println("</tr></table>");
    }
}
