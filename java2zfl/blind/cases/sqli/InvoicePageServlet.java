package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/invoices")
public class InvoicePageServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        int page = parseOr(request.getParameter("page"), 1);
        int size = Math.min(parseOr(request.getParameter("size"), 20), 100);
        int offset = Math.max(page - 1, 0) * size;
        String sql = "SELECT number, issued_on, amount FROM invoices ORDER BY issued_on DESC LIMIT " + size
                + " OFFSET " + offset;
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getString(1) + " " + rs.getDate(2) + " " + rs.getBigDecimal(3));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }

    private static int parseOr(String value, int fallback) {
        if (value == null) {
            return fallback;
        }
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            return fallback;
        }
    }
}
