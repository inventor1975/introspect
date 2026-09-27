package blind.xss.catalog;

import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/price")
public class CurrencyServlet extends HttpServlet {

    private static final Map<String, String> SYMBOLS = Map.of(
            "USD", "$",
            "EUR", "&euro;",
            "GBP", "&pound;",
            "JPY", "&yen;");

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String currency = req.getParameter("currency");
        String amountParam = req.getParameter("amount");
        String symbol = SYMBOLS.getOrDefault(currency == null ? "USD" : currency.toUpperCase(), "$");
        BigDecimal amount;
        try {
            amount = new BigDecimal(amountParam).setScale(2, RoundingMode.HALF_UP);
        } catch (NumberFormatException | NullPointerException e) {
            amount = BigDecimal.ZERO;
        }
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<span class=\"price\">" + symbol + amount.toPlainString() + "</span>");
    }
}
