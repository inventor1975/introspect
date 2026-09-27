package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/insurance/claims")
public class ClaimsSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String status = req.getParameter("status");
        String adjuster = req.getParameter("adjuster");
        String from = req.getParameter("from");

        StringBuilder sql = new StringBuilder("SELECT claim_no, amount FROM claims WHERE 1=1");
        try {
            if (status != null && !status.isBlank()) {
                sql.append(" AND status = '").append(status.trim()).append('\'');
            }
            if (adjuster != null && !adjuster.isBlank()) {
                sql.append(" AND adjuster_id = ").append(Long.parseLong(adjuster.trim()));
            }
            if (from != null && !from.isBlank()) {
                sql.append(" AND filed_on >= DATE '").append(LocalDate.parse(from.trim())).append('\'');
            }
        } catch (NumberFormatException | DateTimeParseException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "invalid filter");
            return;
        }
        sql.append(" ORDER BY filed_on DESC LIMIT 100");

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql.toString())) {
            while (rs.next()) {
                out.println(rs.getLong(1) + "\t" + rs.getBigDecimal(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
