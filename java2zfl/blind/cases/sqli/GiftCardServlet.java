package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Collections;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/giftcards")
public class GiftCardServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        StringBuilder where = new StringBuilder(" WHERE 1=1");
        for (String name : Collections.list(request.getParameterNames())) {
            if (!name.startsWith("f_")) {
                continue;
            }
            String column = name.substring(2);
            if (!column.equals("batch") && !column.equals("issuer")) {
                continue;
            }
            where.append(" AND ").append(column).append(" = '").append(request.getParameter(name)).append("'");
        }
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT card_no, balance FROM gift_cards" + where)) {
            while (rs.next()) {
                out.println(rs.getString(1) + " " + rs.getBigDecimal(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
