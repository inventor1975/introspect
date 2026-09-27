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

@WebServlet("/finance/payments/lookup")
public class PaymentLookupServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String ref = req.getParameter("ref");
        if (ref == null || ref.isBlank()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        ref = ref.trim();
        boolean internalId = ref.chars().allMatch(Character::isDigit);
        String sql = internalId
                ? "SELECT id, amount_cents, state FROM payments WHERE id = " + ref
                : "SELECT id, amount_cents, state FROM payments WHERE psp_reference = '" + ref + "'";

        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            if (!rs.next()) {
                resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                return;
            }
            resp.setContentType("application/json");
            resp.getWriter().print("{\"id\":" + rs.getLong(1) + ",\"amountCents\":" + rs.getLong(2) + "}");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
