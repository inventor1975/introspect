package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/banking/balance")
public class AccountBalanceServlet extends HttpServlet {

    private static final boolean INLINE_SQL_FOR_TRACING = false;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String iban = req.getParameter("iban");
        if (iban == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        long balance;
        try (Connection conn = Db.open()) {
            if (INLINE_SQL_FOR_TRACING) {
                try (Statement st = conn.createStatement();
                     ResultSet rs = st.executeQuery("SELECT balance_cents FROM accounts WHERE iban = '" + iban + "'")) {
                    balance = rs.next() ? rs.getLong(1) : 0L;
                }
            } else {
                try (PreparedStatement ps = conn.prepareStatement("SELECT balance_cents FROM accounts WHERE iban = ?")) {
                    ps.setString(1, iban);
                    try (ResultSet rs = ps.executeQuery()) {
                        balance = rs.next() ? rs.getLong(1) : 0L;
                    }
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain");
        resp.getWriter().print(balance);
    }
}
