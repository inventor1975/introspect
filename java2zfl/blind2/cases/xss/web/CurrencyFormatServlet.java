package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.math.BigDecimal;
import java.text.NumberFormat;
import java.util.Locale;

@WebServlet("/tools/price")
public class CurrencyFormatServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String value = request.getParameter("amount");
        try {
            BigDecimal amount = new BigDecimal(value);
            value = NumberFormat.getCurrencyInstance(Locale.US).format(amount);
        } catch (NumberFormatException | NullPointerException e) {
            value = "$0.00";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<p>Formatted: <b>" + value + "</b></p>");
    }
}
