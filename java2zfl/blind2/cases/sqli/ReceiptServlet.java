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

@WebServlet("/pos/receipt")
public class ReceiptServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String receiptNo = req.getParameter("no");
        try {
            Long.parseLong(receiptNo);
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "receipt number must be numeric");
            return;
        }
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT total_cents, issued_at FROM receipts WHERE receipt_no = " + receiptNo)) {
            if (!rs.next()) {
                resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                return;
            }
            resp.setContentType("text/plain");
            resp.getWriter().println(rs.getLong(1) + " @ " + rs.getTimestamp(2));
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
