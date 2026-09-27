package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Base64;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/giftcards/balance")
public class VoucherBalanceServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String encoded = null;
        if (req.getCookies() != null) {
            for (Cookie cookie : req.getCookies()) {
                if ("gc".equals(cookie.getName())) {
                    encoded = cookie.getValue();
                }
            }
        }
        if (encoded == null) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        String code;
        try {
            code = new String(Base64.getUrlDecoder().decode(encoded), StandardCharsets.UTF_8);
        } catch (IllegalArgumentException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT balance_cents FROM gift_cards WHERE code = '" + code + "'")) {
            resp.setContentType("text/plain");
            resp.getWriter().print(rs.next() ? rs.getLong(1) : 0L);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
