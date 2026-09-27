package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/insurance/claims/filter")
public class ClaimFilterServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String status = req.getParameter("status");
        String adjuster = req.getParameter("adjuster");
        String minAmount = req.getParameter("minAmount");

        StringBuilder sql = new StringBuilder("SELECT claim_no, amount FROM claims WHERE 1=1");
        List<Object> params = new ArrayList<>();
        if (status != null && !status.isBlank()) {
            sql.append(" AND status = ?");
            params.add(status.trim());
        }
        if (adjuster != null && !adjuster.isBlank()) {
            sql.append(" AND adjuster_login = ?");
            params.add(adjuster.trim());
        }
        if (minAmount != null && !minAmount.isBlank()) {
            try {
                params.add(new BigDecimal(minAmount.trim()));
            } catch (NumberFormatException e) {
                resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "minAmount must be a number");
                return;
            }
            sql.append(" AND amount >= ?");
        }
        sql.append(" ORDER BY filed_on DESC LIMIT 100");

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql.toString())) {
            for (int i = 0; i < params.size(); i++) {
                ps.setObject(i + 1, params.get(i));
            }
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.println(rs.getLong(1) + "\t" + rs.getBigDecimal(2));
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
