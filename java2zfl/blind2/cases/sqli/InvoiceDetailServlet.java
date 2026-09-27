package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/billing/invoice")
public class InvoiceDetailServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String idParam = req.getParameter("id");
        int invoiceId;
        try {
            invoiceId = Integer.parseInt(idParam);
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "invalid invoice id");
            return;
        }
        String sql = "SELECT amount_cents, issued_on FROM invoices WHERE id = " + invoiceId;
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            if (!rs.next()) {
                resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                return;
            }
            resp.setContentType("application/json");
            resp.getWriter().print("{\"amountCents\":" + rs.getLong(1) + ",\"issuedOn\":\"" + rs.getDate(2) + "\"}");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
