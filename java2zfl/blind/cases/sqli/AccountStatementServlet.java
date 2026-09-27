package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/statement")
public class AccountStatementServlet extends HttpServlet {

    private static final String PROC = "statement_lines";

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String account = request.getParameter("acct");
        String month = request.getParameter("month");
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect();
             CallableStatement cs = conn.prepareCall("{call " + PROC + "(?, ?)}")) {
            cs.setString(1, account);
            cs.setString(2, month);
            try (ResultSet rs = cs.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getDate(1) + " " + rs.getString(2) + " " + rs.getBigDecimal(3));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
