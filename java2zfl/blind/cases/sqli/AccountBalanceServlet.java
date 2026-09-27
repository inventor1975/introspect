package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/balance")
public class AccountBalanceServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String account = request.getParameter("acct");
        String currency = request.getParameter("ccy");
        if (currency == null) {
            currency = "EUR";
        }
        try (Connection conn = Db.connect();
             CallableStatement cs = conn.prepareCall("{call get_balance('" + account + "', ?)}")) {
            cs.setString(1, currency);
            try (ResultSet rs = cs.executeQuery()) {
                if (rs.next()) {
                    response.getWriter().println(rs.getBigDecimal(1) + " " + currency);
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
