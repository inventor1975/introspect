package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/amounts")
public class AmountColumnServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String[] amounts = req.getParameterValues("amount");
        CellFormatter money = new CurrencyCellFormatter();
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<table class=\"amounts\">");
        if (amounts != null) {
            for (String amount : amounts) {
                out.println("<tr><td class=\"num\">" + money.format(amount) + "</td></tr>");
            }
        }
        out.println("</table>");
    }
}
