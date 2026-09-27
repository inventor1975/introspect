package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Collections;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/billing/invoices/mark-sent")
public class BulkInvoiceServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String[] numbers = req.getParameterValues("invoice");
        if (numbers == null || numbers.length == 0 || numbers.length > 500) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "select between 1 and 500 invoices");
            return;
        }
        String placeholders = String.join(",", Collections.nCopies(numbers.length, "?"));
        String sql = "UPDATE invoices SET status = 'SENT', sent_at = now() WHERE number IN (" + placeholders + ")";
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            for (int i = 0; i < numbers.length; i++) {
                ps.setString(i + 1, numbers[i]);
            }
            int updated = ps.executeUpdate();
            resp.setContentType("text/plain");
            resp.getWriter().println(updated + " invoices marked as sent");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
