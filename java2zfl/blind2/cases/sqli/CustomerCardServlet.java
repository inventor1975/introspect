package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/loyalty/card")
public class CustomerCardServlet extends HttpServlet {

    private static final String TABLE = "loyalty_cards";
    private static final String COLUMNS = "card_no, tier, points";

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String cardNo = req.getParameter("card");
        if (cardNo == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String sql = "SELECT " + COLUMNS + " FROM " + TABLE + " WHERE card_no = ? AND blocked = false";
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, cardNo.trim());
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                    return;
                }
                resp.setContentType("application/json");
                resp.getWriter().print("{\"points\":" + rs.getInt("points") + "}");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
