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
import org.apache.commons.lang3.StringUtils;

@WebServlet("/loyalty/points")
public class LoyaltyPointsServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String account = req.getParameter("account");
        if (!StringUtils.isNumeric(account)) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "account number must be numeric");
            return;
        }
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT points FROM loyalty_accounts WHERE account_no = " + account)) {
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.next() ? rs.getInt(1) : 0);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
