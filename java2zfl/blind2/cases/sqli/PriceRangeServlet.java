package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/products/by-price")
public class PriceRangeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        BigDecimal min;
        BigDecimal max;
        try {
            min = new BigDecimal(req.getParameter("min"));
            max = new BigDecimal(req.getParameter("max"));
        } catch (NumberFormatException | NullPointerException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "min and max are required numbers");
            return;
        }
        String sql = "SELECT id FROM products WHERE active = true AND price BETWEEN " + min.toPlainString()
                + " AND " + max.toPlainString() + " ORDER BY price";

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
