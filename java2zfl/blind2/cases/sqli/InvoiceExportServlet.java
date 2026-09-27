package blind2.sqli;

import blind2.sqli.support.Db;
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

@WebServlet("/billing/invoices/export")
public class InvoiceExportServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String[] numbers = req.getParameterValues("invoice");
        if (numbers == null || numbers.length == 0) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "no invoices selected");
            return;
        }
        String inList = "'" + String.join("','", numbers) + "'";
        String sql = "SELECT id, issued_on, amount FROM invoices WHERE number IN (" + inList + ") ORDER BY issued_on";

        resp.setContentType("text/csv");
        resp.setHeader("Content-Disposition", "attachment; filename=invoices.csv");
        PrintWriter out = resp.getWriter();
        out.println("id,issued_on,amount");
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + "," + rs.getDate(2) + "," + rs.getBigDecimal(3));
            }
        } catch (SQLException e) {
            throw new ServletException("export failed", e);
        }
    }
}
